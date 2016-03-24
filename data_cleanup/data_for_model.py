from file_parsing import json_parse, city_data, comb_id_reviews, sent_split
from file_parsing import ind_sentences
from collections import Counter
from nltk.tokenize import RegexpTokenizer
import cPickle as pickle
import unicodedata
import nltk


# Pull menu list out of restaurant data
def get_menu_list(rest_data):
    menu_list = []
    for rest in rest_data:
        for item in rest['items']:
            menu_list.append(item['name'])
    menu_list = list(set(menu_list))
    return menu_list


# Pos tag all menu items
def pos_list(menu_list):
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


# Return only most common words from total pos_list, 45 was chosen based on views of the word counts
def common_words(pos_list):
    cnt = Counter(pos_list)
    new_dict = dict((k, v) for k, v in cnt.items() if v >= 45)
    word_list = new_dict.keys()
    return [word for word in word_list if len(word) > 2]


# Return only sentences containing words from word list
def sent_check(sentences, word_list):
    tokenizer = RegexpTokenizer(r'\w+')
    sentences_to_test = []
    for sent in sentences:
        if any(word in tokenizer.tokenize(sent.lower()) for word in word_list):
            sentences_to_test.append(sent)
    return sentences_to_test

if __name__ == '__main__':
    rest_data = json_parse('../cs224n-food/data/restaurants.json')
    rev_data = json_parse('../cs224n-food/data/reviews.json')

    # Getting SF data only
    id_list, sf_rest, sf_rev = city_data(rest_data, rev_data, 'sf')

    # Creating a tuple of business id and individual review for reviews greater than or equal to 4
    reviews_comb = comb_id_reviews(sf_rev)

    # Splitting reviews into sentences
    reviews_split = sent_split(reviews_comb)

    # Getting all individual sentences
    sentences = ind_sentences(reviews_split)

    # Get menus for all SF restaurants
    menu_list = get_menu_list(sf_rest)

    # Get pos tags for all menu items
    new_pos_list, pos_list = pos_list(menu_list)

    # Return only most common words from SF menu bag of words
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

    # Create data to train and test the model (**running this will attain different results since
    # I did not use a random state number when initially performing this step**)

    ## Create training data
    # test_sent = random.sample(sentences_to_check, 500)
    # test_g_1 = test_sent[:100]
    # test_g_2 = test_sent[100:200]
    # test_g_3 = test_sent[200:300]
    # test_g_4 = test_sent[300:400]
    # test_g_5 = test_sent[400:500]

    # pos_tag_lst1 = pos_tagger(test_g_1)
    # pos_tag_lst2 = pos_tagger(test_g_2)
    # pos_tag_lst3 = pos_tagger(test_g_3)
    # pos_tag_lst4 = pos_tagger(test_g_4)
    # pos_tag_lst5 = pos_tagger(test_g_5)

    # with open("../data/pos_tag_lst1.pkl", "w") as fp:
    #     pickle.dump(pos_tag_lst1, fp)
    # with open("../data/pos_tag_lst2.pkl", "w") as fp:
    #     pickle.dump(pos_tag_lst2, fp)
    # with open("../data/pos_tag_lst3.pkl", "w") as fp:
    #     pickle.dump(pos_tag_lst3, fp)
    # with open("../data/pos_tag_lst4.pkl", "w") as fp:
    #     pickle.dump(pos_tag_lst4, fp)
    # with open("../data/pos_tag_lst5.pkl", "w") as fp:
    #     pickle.dump(pos_tag_lst5, fp)

    # with open("../data/sent_list_1.pkl", "w") as fp:
    #     pickle.dump(test_g_1, fp)
    # with open("../data/sent_list_2.pkl", "w") as fp:
    #     pickle.dump(test_g_2, fp)
    # with open("../data/sent_list_3.pkl", "w") as fp:
    #     pickle.dump(test_g_3, fp)
    # with open("../data/sent_list_4.pkl", "w") as fp:
    #     pickle.dump(test_g_4, fp)
    # with open("../data/sent_list_5.pkl", "w") as fp:
    #     pickle.dump(test_g_5, fp)

    ## Create testing data
    # overall_test = random.sample(sentences, 100)
    # pos_overall = pos_tagger(overall_test)
    # with open("../data/pos_overall.pkl", "w") as fp:
    #     pickle.dump(pos_overall, fp)
    # with open("../data/sent_overall.pkl", "w") as fp:
    #     pickle.dump(overall_test, fp)
