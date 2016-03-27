import sklearn_crfsuite
import cPickle as pickle
from sklearn.metrics import make_scorer
from sklearn.metrics import recall_score
from sklearn.grid_search import GridSearchCV
from sklearn.externals import joblib
from sklearn_crfsuite.utils import flatten


def word2features(sent, i):
    '''Define word features'''
    word = sent[i][0]
    postag = sent[i][1]
    features = {
        'bias': 1.0,
        'word.lower()': word.lower(),
        'word[-3:]': word[-3:],
        'word[-2:]': word[-2:],
        'word.isupper()': word.isupper(),
        'word.istitle()': word.istitle(),
        'word.isdigit()': word.isdigit(),
        'postag': postag,
        'postag[:2]': postag[:2],
    }
    if i > 0:
        word1 = sent[i-1][0]
        postag1 = sent[i-1][1]
        features.update({
            '-1:word.lower()': word1.lower(),
            '-1:word.istitle()': word1.istitle(),
            '-1:word.isupper()': word1.isupper(),
            '-1:word.isdigit()': word1.isdigit(),
            '-1:postag': postag1,
            '-1:postag[:2]': postag1[:2],
        })
    if i > 1:
        word1 = sent[i-1][0]
        postag1 = sent[i-1][1]
        word2 = sent[i-2][0]
        postag2 = sent[i-2][1]
        features.update({
            '-1:word.lower()': word1.lower(),
            '-1:word.istitle()': word1.istitle(),
            '-1:word.isupper()': word1.isupper(),
            '-1:word.isdigit()': word1.isdigit(),
            '-1:postag': postag1,
            '-1:postag[:2]': postag1[:2],
            '-2:word.lower()': word2.lower(),
            '-2:word.istitle()': word2.istitle(),
            '-2:word.isupper()': word2.isupper(),
#             '-2:word.isdigit()': word2.isdigit(),
            '-2:postag': postag2,
            '-2:postag[:2]': postag2[:2],
        })
    else:
        features['BOS'] = True
    if i < len(sent)-1:
        word1 = sent[i+1][0]
        postag1 = sent[i+1][1]
        features.update({
            '+1:word.lower()': word1.lower(),
            '+1:word.istitle()': word1.istitle(),
            '+1:word.isupper()': word1.isupper(),
            '+1:postag': postag1,
            '+1:postag[:2]': postag1[:2],
        })
    if i < len(sent)-2:
        word1 = sent[i+1][0]
        postag1 = sent[i+1][1]
        word2 = sent[i+2][0]
        postag2 = sent[i+2][1]
        features.update({
            '+1:word.lower()': word1.lower(),
            '+1:word.istitle()': word1.istitle(),
            '+1:word.isupper()': word1.isupper(),
            '+1:postag': postag1,
            '+1:postag[:2]': postag1[:2],
#             '+2:word.lower()': word2.lower(),
#             '+2:word.istitle()': word2.istitle(),
#             '+2:word.isupper()': word2.isupper(),
#             '+2:postag': postag2,
#             '+2:postag[:2]': postag2[:2],
        })
    else:
        features['EOS'] = True
    return features


def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]


def sent2labels(sent):
    return [label for token, postag, label in sent]


def sent2tokens(sent):
    return [token for token, postag, label in sent]


def metrics(y_pred, y_test):
    '''Define metrics - F1, Precision, and Recall'''
    pred = []
    for x in y_pred:
        if any(y == 'FOOD' for y in x):
            pred.append(1)
        else:
            pred.append(0)
    tester = []
    for x in y_test:
        if any(y == 'FOOD' for y in x):
            tester.append(1)
        else:
            tester.append(0)
    tp = 0
    fp = 0
    tn = 0
    fn = 0
    for grp in zip(pred, tester):
        if grp[0] == 1:
            if grp[1] == 1:
                tp += 1
        if grp[0] == 1:
            if grp[1] == 0:
                fp += 1
        if grp[0] == 0:
            if grp[1] == 0:
                tn += 1
        if grp[0] == 0:
            if grp[1] == 1:
                fn += 1
    recall = float(tp)/(tp+fn)
    precision = float(tp)/(tp+fp)
    f1 = float(tp*2)/(tp*2+fp+fn)
    return recall, precision, f1


def flat_recall(y_true, y_pred):
    '''Define flat recall metric'''
    ytr_flat = flatten(y_true)
    ypr_flat = flatten(y_pred)
    return recall_score(ytr_flat, ypr_flat, pos_label="FOOD",
        average='binary')

if __name__ == '__main__':
    # Load data from pickled files
    with open('../data/post_proc_pkl/sent_final_1.pkl', 'rb') as fp:
        sent_final_1 = pickle.load(fp)
    with open('../data/post_proc_pkl/sent_final_2.pkl', 'rb') as fp:
        sent_final_2 = pickle.load(fp)
    with open('../data/post_proc_pkl/sent_final_3.pkl', 'rb') as fp:
        sent_final_3 = pickle.load(fp)
    with open('../data/post_proc_pkl/sent_final_4.pkl', 'rb') as fp:
        sent_final_4 = pickle.load(fp)
    with open('../data/post_proc_pkl/sent_final_55.pkl', 'rb') as fp:
        sent_final_55 = pickle.load(fp)
    with open('../data/post_proc_pkl/sent_final_510.pkl', 'rb') as fp:
        sent_final_510 = pickle.load(fp)
    with open('../data/post_proc_pkl/sent_overall_test.pkl', 'rb') as fp:
        sent_overall_test = pickle.load(fp)

    # Separate data into train and test
    train_sents = sent_final_1 + sent_final_2 + sent_final_3 + sent_final_4 +sent_final_55 + sent_final_510
    test_sents = sent_overall_test

    # Extract the features from the data
    X_train = [sent2features(s) for s in train_sents]
    y_train = [sent2labels(s) for s in train_sents]
    X_test = [sent2features(s) for s in test_sents]
    y_test = [sent2labels(s) for s in test_sents]

    # Fit the model
    crf = sklearn_crfsuite.CRF(
        algorithm='lbfgs',
        max_iterations=100)
    # Use a full grid over all parameters
    param_grid = {"c1": [.1, .01, .001, .0001],
                  "c2": [.1, .01, .001, .0001],
                  "all_possible_transitions": [True, False]}

    # Run grid search
    recall_scorer = make_scorer(flat_recall)
    grid_search = GridSearchCV(crf, param_grid=param_grid, cv=5, scoring=recall_scorer)
    grid_search.fit(X_train, y_train)

    # Make predictions on the test data using the model
    new_crf = grid_search.best_estimator_
    y_pred = new_crf.predict(X_test)
    print metrics(y_pred, y_test)
    print grid_search.best_params_

    # Pickle the model
    joblib.dump(new_crf, 'model_name.pkl')
