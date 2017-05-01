# Load model data into hosted EC2 PostGRES table
import nltk
import unicodedata
from file_parsing import duplicate_rest
from file_parsing import pos_tagger
from model import word2features, sent2features
from sklearn.externals import joblib
from fuzzywuzzy import fuzz
from collections import Counter
import psycopg2
import cPickle as pickle


def get_only_rest_w_menu(rest_data, rev_data):
    """Get only restaurants that have a menu listed in the dataset."""
    rest_data_w_menus = [rest for rest in rest_data if rest['items']]
    id_list = [rest['id'] for rest in rest_data_w_menus]
    rev_data_w_menus = [rev for rev in rev_data if rev['id'] in id_list]
    return id_list, rest_data_w_menus, rev_data_w_menus


def rp_comb_id_reviews(rev_data):
    """Only get reviews that are greater than or equal to 4 stars."""
    list_revs = [rev['comment'] for rev in rev_data['reviews'] if rev['rating'] >= 4]
    return list_revs


def rp_sent_split(list_revs):
    """Split reviews into sentences."""
    rev_sent = []
    for review in list_revs:
        sent = unicodedata.normalize('NFKD', review).encode('ascii', 'ignore')
        sent = nltk.sent_tokenize(sent, language="english")
        rev_sent.append(sent)
    return rev_sent


def rp_ind_sentences(rev_sent):
    """Add indexes to review sentences."""
    sent_list = []
    for review in rev_sent:
        sent_list.extend(review)
    sent_list = [(i, row) for i, row in enumerate(sent_list)]
    return sent_list


def get_menu(specific_rest):
    """Clean data from restaurant menus."""
    drinks_to_remove = ['Sodas',
                        'Bottled Water',
                        'Tomato Juice',
                        'San Pellegrino Sparkling Mineral Water',
                        'Coffee', 'Tea', 'Cappuccino', 'Water', 'Soda',
                        'Juice', 'Coke', 'Cola', 'Coca-Cola', 'Sprite',
                        'Ginger Ale', 'Beer', 'Milk', 'Feta', 'Bread', 'Rice',
                        'Soup of the day', 'Caesar Salad']
    menu = []
    for item in specific_rest['items']:
        name = unicodedata.normalize('NFKD', item['name']).encode('ascii', 'ignore')
        menu.append(name)
    new_menu = [item for item in menu if item not in drinks_to_remove]
    return new_menu


def ner_food(predictions, sentences):
    """Return a list of the sentences that were tagged to have a food entity."""
    list_pred = []
    for i, x in enumerate(predictions):
        if any(y == "FOOD" for y in x):
            list_pred.append(sentences[i])
    return list_pred


def menu_count(food_sents, rest_menu):
    """Return a count of menu items and how often they were tagged."""
    blank_list = []
    for sent in (food_sents):
        if len(sent) <= 150:
            for x in rest_menu:
                if fuzz.partial_ratio(sent, x) >= 75:
                    blank_list.append(x)
        else:
            for x in rest_menu:
                if fuzz.token_set_ratio(sent, x) >= 68:
                    blank_list.append(x)
    return Counter(blank_list)


if __name__ == '__main__':
    # Load model
    crf = joblib.load('final_model.pkl')

    # Load data
    with open('../data/rev_data.pkl', 'rb') as fp:
        rev_data = pickle.load(fp)
    with open('../data/rest_data.pkl', 'rb') as fb:
        rest_data = pickle.load(fb)

    # Remove chains and restaurants without menus
    id_list, city_rest_data, city_rev_data = duplicate_rest(rest_data,
                                                            rev_data)
    id_list, city_rest_data, city_rev_data = get_only_rest_w_menu(city_rest_data, city_rev_data)

    # Make predictions for all valid restaurants, perform menu matching and load data into a POSTgres database
    for rest, revs in zip(city_rest_data, city_rev_data):
        revs = rp_comb_id_reviews(revs)
        sentences = rp_sent_split(revs)
        sent_cntr = rp_ind_sentences(sentences)
        pos_tags = pos_tagger(sent_cntr)
        X_test = [sent2features(s) for s in pos_tags]

        # Get menu
        rest_menu = get_menu(rest)

        # Predict text entity types
        predictions = crf.predict(X_test)

        # Pick out sentences with food
        food_sents = ner_food(predictions, sent_cntr)

        # Get counter of popular food at restaurant X
        vals_dict = menu_count(food_sents, rest_menu)

        # Load data into POSTgres
        if vals_dict:
            rest_dict = {'rest_id': rest['id'], 'city': rest['city'],
                         'rest_name': rest['name'], 'menu': vals_dict}
            conn = psycopg2.connect(dbname='yelp', user='postgres', host='/tmp')
            c = conn.cursor()
            for x in rest_dict['menu']:
                c.execute("""INSERT INTO restaurants (rest_id, city, rest_name, menu_item, menu_section, count)
                        VALUES
                        (%s, %s, %s, %s, NULL, %s); """,
                        (rest_dict['rest_id'], rest_dict['city'].upper(), rest_dict['rest_name'], x, rest_dict['menu'][x]))
                conn.commit()
            conn.close()
