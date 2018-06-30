import cPickle as pickle
from features.vectorizer import PolitenessFeatureVectorizer
import os
import numpy as np
from scipy.sparse import csr_matrix


useful_data = dict()
names = dict()


MODEL_FILENAME = os.path.join(os.path.split(__file__)[0], 'politeness-svm.p')

####
# Load model, initialize vectorizer

clf = pickle.load(open(MODEL_FILENAME))
vectorizer = PolitenessFeatureVectorizer()


def get_politeness(comment):
    doc = dict()
    doc['text'] = comment
    doc['sentences'] = [comment]
    features = vectorizer.features(doc)
    fv = [features[f] for f in sorted(features.iterkeys())]
    # Single-row sparse matrix
    X = csr_matrix(np.asarray([fv]))
    probs = clf.predict_proba(X)
    return probs[0][1]
