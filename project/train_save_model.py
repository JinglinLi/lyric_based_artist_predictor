"""
This script is used to train the model that can predict
artist based on given lyric text, using the data scraped
with artist_lyric_scraper.py. The final model is saved in
artist_predictor.pkl.
"""

import pandas as pd
import numpy as np
import glob
from sklearn.feature_extraction.text import TfidfVectorizer
from imblearn.over_sampling import RandomOverSampler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline, Pipeline
import joblib
from TextCleaner import TextCleaner


def get_corpus_labels(artists, path):
    '''input : artists str-list 
               path str path to the artist folders containting lyrics txt files
       return : corpus list each row a str with lyrics of one song
                labels list each row a str of artist name'''
    corpus = []
    labels = []
    labels_n = []
    for i_artist in range(len(artists)):
        artist = artists[i_artist] 
        path_filenames = (path + f'/{artist}/' + f'{artist}_lyric_*.txt')
        song_files = [f for f in sorted(glob.glob(path_filenames))]
        for i in range(len(song_files)):
            text = open(song_files[i], 'r').read()
            corpus.append(text)
            labels.append(artist) # string labels
            labels_n.append(i_artist) # 0,1 labels
    return corpus, labels, labels_n


# combine lyrics of two artist to one corpus
artists = ['simon_garfunkel', 'queen']
path = '/Users/jinglin/Documents/spiced_projects/unsupervised-lemon-student-code/week_04/project'
(corpus, labels, labels_n) = get_corpus_labels(artists, path)


# feature and label/target value
X = pd.DataFrame({'lyric' : corpus})
y = pd.DataFrame({'artist' : labels})


# train test split
Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=0.25, random_state=0)


# deal with class imbalance 
# original Xtrain simon_garfunkel 151, queen 402; increase simon_garfunkel to 250
ros = RandomOverSampler(sampling_strategy={'simon_garfunkel' : 250}, random_state=0)
X_ros, y_ros = ros.fit_resample(Xtrain, ytrain)


# feature englineering pipeline 
fe_pipe = make_pipeline(
    TextCleaner(), 
    TfidfVectorizer(stop_words='english', max_df=0.8, min_df=0.01, ngram_range=(1,2))
)


# feature engineering - machine learning pipeline 
fe_ml_pipe = Pipeline([
    ('fe', fe_pipe),
    ('logreg', LogisticRegression(random_state=0))
])


# train 
fe_ml_pipe.fit(Xtrain['lyric'].tolist(), ytrain['artist'].tolist())
train_score = fe_ml_pipe.score(Xtrain['lyric'].tolist(), np.ravel(ytrain))


# test 
test_score = fe_ml_pipe.score(Xtest['lyric'].tolist(), np.ravel(ytest))
print(train_score, test_score)


# save model
joblib.dump(fe_ml_pipe, 'artist_predictor.pkl') 
