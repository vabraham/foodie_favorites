# Run this script to perform word annotation for training/testing models
from file_parsing import tag_words_crf
import cPickle as pickle


def word_annotation(pos_tag_fn, sent_list_fn, final_pos_tag_fn):
    """Process tagged lines.

    Inputs for the function should be the relative paths to the pickle.

    files:
            ex pos_tag_fn: '../data/pre_proc_pkl/pos_tag_list_5.pkl'
            ex sent_list_fn: '../data/pre_proc_pkl/sent_list_5.pkl'
            ex final_pos_tag_fn (to-be location): '../data/post_proc_pkl/sent_final_5.pkl'
    """
    with open(pos_tag_fn, 'rb') as fp:
        pos_tag_list = pickle.load(fp)
    with open(sent_list_fn, 'rb') as fp:
        sent_list = pickle.load(fp)
    final_post_tag = tag_words_crf(pos_tag_list, sent_list)
    with open(final_pos_tag_fn, 'w') as fp:
        pickle.dump(final_post_tag, fp)
