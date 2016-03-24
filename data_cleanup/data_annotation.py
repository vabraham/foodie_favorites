# Run this script to perform word annotation for training/testing models
from file_parsing import tag_words_crf
import cPickle as pickle


def word_annotation(pos_tag_fn, sent_list_fn, final_pos_tag_fn):
    with open(pos_tag_fn, 'rb') as fp:
        pos_tag_list = pickle.load(fp)
    with open(sent_list_fn, 'rb') as fp:
        sent_list = pickle.load(fp)
    final_post_tag = tag_words_crf(pos_tag_list, sent_list)
    with open(final_pos_tag_fn, 'w') as fp:
        pickle.dump(final_post_tag, fp)

# if __name__ == '__main__':
#     with open('../data/pos_tag_lst5.pkl', 'rb') as fp:
#         pos_tag_list510 = pickle.load(fp)
#     with open('../data/sent_list_5.pkl', 'rb') as fp:
#         sent_list_510 = pickle.load(fp)
#     sent_final_510 = tag_words_crf(pos_tag_list510[50:], sent_list_510[50:])
#     with open("../data/sent_final_510.pkl", "w") as fp:
#         pickle.dump(sent_final_510, fp)
