from sklearn.base import BaseEstimator, TransformerMixin
import re

class TextCleaner(BaseEstimator, TransformerMixin):
    ''' text cleaning : 
        input can be str, list of sring, or pandas Series 
        a minimal version, repacing only '\n' with ' '
    '''

    def __init__(self):
        print('')

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        ''' text cleaning : input can be str, list of sring, or pandas Series '''
        if isinstance(X, str): # e.g. "hello darkness my old friend"
            X_ = re.sub(r'\n', ' ', X.lower())
        elif isinstance(X, list): # e.g. Xtrain['lyric'].tolist()
            X_ = [x.replace('\n', ' ') for x in X]
        else: # e.g. Xtrain['lyric']
            X_ = [re.sub(r'\n', ' ', x.lower()) for x in X]
        return X_

