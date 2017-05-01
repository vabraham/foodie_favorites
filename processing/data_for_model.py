# Run this script to pre-process training data
from file_parsing import json_parse, duplicate_rest, comb_id_reviews
from file_parsing import ind_sentences, sent_split, pos_tagger
from collections import Counter
from nltk.tokenize import RegexpTokenizer
import cPickle as pickle
import unicodedata
import nltk
import random


def get_menu_list(rest_data):
    """Pull menu list out of restaurant data."""
    menu_list = []
    for rest in rest_data:
        for item in rest['items']:
            menu_list.append(item['name'])
    menu_list = list(set(menu_list))
    return menu_list


def pos_list(menu_list):
    """Part of speech tag all menu items."""
    pos_list = []
    for line in menu_list:
        line = unicodedata.normalize('NFKD', line).encode('ascii', 'ignore')
        words = nltk.pos_tag(line.split())
        for word in words:
            if word[1] in ('NN', 'NNP'):
                pos_list.append(word[0].strip("()"))
    new_pos_list = list(set([word.lower() for word in pos_list]))
    pos_list = [word.lower() for word in pos_list]
    return new_pos_list, pos_list


def common_words(pos_list):
    """Return only most common words from total pos_list, 45 was chosen based on views of the word counts."""
    cnt = Counter(pos_list)
    new_dict = dict((k, v) for k, v in cnt.items() if v >= 45)
    word_list = new_dict.keys()
    return [word for word in word_list if len(word) > 2]


def sent_check(sentences, word_list):
    """Return only sentences containing words from word list."""
    toke = RegexpTokenizer(r'\w+')
    sentences_to_test = []
    for sent in sentences:
        if any(word in toke.tokenize(sent.lower()) for word in word_list):
            sentences_to_test.append(sent)
    return sentences_to_test

if __name__ == '__main__':
    # Load data
    # The below files need to be unzipped from Yelp_data_json_2006_2012.zip
    rest_data = json_parse('../data/restaurants.json')
    rev_data = json_parse('../data/reviews.json')

    # Remove duplicates (ex. chain restaurants)
    id_list, rest, rev = duplicate_rest(rest_data, rev_data)

    # Creating a tuple of business id and individual review for reviews >= 4 stars
    reviews_comb = comb_id_reviews(rev)

    # Splitting reviews into sentences
    reviews_split = sent_split(reviews_comb)

    # Getting all individual sentences
    sentences = ind_sentences(reviews_split)

    # Get menus for all restaurants
    menu_list = get_menu_list(rest)

    # Get POS tags for all menu items
    new_pos_list, pos_list = pos_list(menu_list)

    # Return only most common words from bag of words
    word_list = common_words(pos_list)
    words_to_remove = ['special', 'won', 'soda', 'snow', 'pcs.', 'noodles,', 'family', 'seafood', 'noodles,']
    word_list = [word for word in word_list if word not in words_to_remove]

    # Pickle the common word list
    with open("../data/word_list.pkl", "w") as fp:
        pickle.dump(word_list, fp)

    # Return only sentences containing words from the word list, this will create a better model for future predictions
    sentences_to_check = sent_check(sentences, word_list)

    # Pickle the updated sentence list
    with open("../data/sent_list_from_wl.pkl", "w") as fp:
        pickle.dump(sentences_to_check, fp)

    # Create data to train and test the model (**running this will attain different results since I did not use a random state number when initially performing this step**)
    test_sent = random.sample(sentences_to_check, 500)
    test_g_1 = test_sent[:100]
    test_g_2 = test_sent[100:200]
    test_g_3 = test_sent[200:300]
    test_g_4 = test_sent[300:400]
    test_g_5 = test_sent[400:500]

    pos_tag_list_1 = pos_tagger(test_g_1)
    pos_tag_list_2 = pos_tagger(test_g_2)
    pos_tag_list_3 = pos_tagger(test_g_3)
    pos_tag_list_4 = pos_tagger(test_g_4)
    pos_tag_list_5 = pos_tagger(test_g_5)

    # Pickle all POS tagged sentences and original sentences
    with open("../data/pre_proc_pkl/pos_tag_list_1.pkl", "w") as fp:
        pickle.dump(pos_tag_list_1, fp)
    with open("../data/pre_proc_pkl/pos_tag_list_2.pkl", "w") as fp:
        pickle.dump(pos_tag_list_2, fp)
    with open("../data/pre_proc_pkl/pos_tag_list_3.pkl", "w") as fp:
        pickle.dump(pos_tag_list_3, fp)
    with open("../data/pre_proc_pkl/pos_tag_list_4.pkl", "w") as fp:
        pickle.dump(pos_tag_list_4, fp)
    with open("../data/pre_proc_pkl/pos_tag_list_5.pkl", "w") as fp:
        pickle.dump(pos_tag_list_5, fp)
    with open("../data/pre_proc_pkl/sent_list_1.pkl", "w") as fp:
        pickle.dump(test_g_1, fp)
    with open("../data/pre_proc_pkl/sent_list_2.pkl", "w") as fp:
        pickle.dump(test_g_2, fp)
    with open("../data/pre_proc_pkl/sent_list_3.pkl", "w") as fp:
        pickle.dump(test_g_3, fp)
    with open("../data/pre_proc_pkl/sent_list_4.pkl", "w") as fp:
        pickle.dump(test_g_4, fp)
    with open("../data/pre_proc_pkl/sent_list_5.pkl", "w") as fp:
        pickle.dump(test_g_5, fp)

    # Create and pickle test data (**running this will attain different results since I did not use a random state number when initially performing this step**)
    sent_overall = random.sample(sentences, 100)
    pos_overall = pos_tagger(sent_overall)
    with open("../data/pre_proc_pkl/pos_overall.pkl", "w") as fp:
        pickle.dump(pos_overall, fp)
    with open("../data/pre_proc_pkl/sent_overall.pkl", "w") as fp:
        pickle.dump(sent_overall, fp)
