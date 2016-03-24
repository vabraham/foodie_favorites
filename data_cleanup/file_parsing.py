import json
import nltk
import unicodedata
import random
import re


# Load the json files into a python readable format
def json_parse(filename):
    new_list = []
    with open(filename) as fn:
        for line in fn:
            new_list.append(json.loads(line))
    return new_list


# Remove restaurant chains and duplicates
def duplicate_rest(rest_data, rev_data):
    # city set
    # {u'boston', u'chicago', u'la', u'nyc', u'philadelphia', u'sf', u'washington'}
    restaurants_to_remove = ["Applebee's",
                             "Arby's",
                             'Au Bon Pain',
                             'Bagelworks',
                             "Baluchi's",
                             'Baskin-Robbins',
                             'Bistro Burger',
                             'Burger King',
                             'Caribou Coffee',
                             "Carl's Jr.",
                             'Chipotle',
                             'Cold Stone Creamery',
                             'Del Taco',
                             "Denny's",
                             "Domino's Pizza",
                             "Dunkin' Donuts",
                             'El Pollo Loco',
                             'Finagle A Bagel',
                             "Giacomo's Ristorante",
                             'Haagen Dazs',
                             'Hooters',
                             'IHOP',
                             'In-N-Out',
                             'Jack in the Box',
                             'Jamba Juice',
                             "Jimbo's Hamburger Palace",
                             'KFC - Kentucky Fried Chicken',
                             'La Cocina',
                             'Lite Delights',
                             "McDonald's",
                             "Mel's Drive In",
                             'Mels Drive-in',
                             "Noah's",
                             "Papa John's Pizza",
                             "Pepe's Mexican Restaurant",
                             'Pizza Hut',
                             'Popeyes Chicken & Biscuits',
                             'Quiznos Sub',
                             "Rita's Ice Custard Happiness",
                             'Soup Man',
                             'Starbucks Coffee',
                             'Subway',
                             'The Coffee Bean & Tea Leaf',
                             "Tully's Coffee",
                             "Wendy's"]
    city_rest_data = [rest for rest in rest_data if rest['name'] not in restaurants_to_remove]
    id_list = [rest['id'] for rest in city_rest_data]
    city_rev_data = [rev for rev in rev_data if rev['id'] in id_list]
    return id_list, city_rest_data, city_rev_data


# Create tuple of business id and individual review for all review ratings >= 4
def comb_id_reviews(rev_data):
    list_revs = []
    for i in xrange(len(rev_data)):
        for review in rev_data[i]['reviews']:
            if review['rating'] >= 4:
                list_revs.append((rev_data[i]['id'], review['comment']))
    return list_revs


# Split individual reviews into sentences - format (review id, [sentences])
def sent_split(list_revs):
    rev_sent = []
    for review in list_revs:
        sent = unicodedata.normalize('NFKD', review[1]).encode('ascii', 'ignore')
        sent = nltk.sent_tokenize(sent, language="english")
        rev_sent.append((review[0], sent))
    return rev_sent


# Append an index value to all sentences
def ind_sentences(rev_sent):
    sent_list = []
    for review in rev_sent:
        sent_list.extend(review[1])
    i = 0
    for row in sent_list:
        i += 1
        row = (i, row)
    return sent_list


# Take a random sample of sentences (for model training and testing)
def randomize_sentences(sent_list, sample_size):
    random_indices = random.sample(xrange(len(sent_list)), sample_size)
    random_sent = [sent_list[x] for x in random_indices]
    return random_sent


# POS tag all words in each sentence
def pos_tagger(sent_list):
    pos_tag_list = []
    for sentence in sent_list:
        pos_tag_list.append(nltk.pos_tag(re.findall(r"[\w']+|[(.,!?;)]", sentence)))
    return pos_tag_list


# Allow users to manually tag whether words in sentences are "FOOD" or "OTHER"
def tag_words_crf(pos_tag_list, sent_list):
    i = -1
    for pos in pos_tag_list:
        i += 1
        print sent_list[i]
        print "Index %s" % i
        for j, indx in enumerate(pos):
            print "Classification for %r, (F)OOD or (O)ther?" % str(indx)
            val = raw_input("> ").lower()
            if val == 'f':
                pos[j] = indx + ("FOOD",)
            else:
                pos[j] = indx + ("O",)
    return pos_tag_list


# if __name__ == '__main__':
#     rest_data = json_parse('../cs224n-food/data/restaurants.json')
#     rev_data = json_parse('../cs224n-food/data/reviews.json')

#     # with open("../data/rest_data.pkl", "w") as fp:
#     #     pickle.dump(rest_data, fp)

#     # with open("../data/rev_data.pkl", "wb") as fp:
#     #     pickle(rev_data, fp)

#     city_list = set([rest['city'] for rest in rest_data])
#     # city_list = {u'boston', u'chicago', u'la', u'nyc', u'philadelphia', u'sf', u'washington'}
