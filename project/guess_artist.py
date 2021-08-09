"""
This script is a command interface for predicting artist 
based on user input lyric string. The model used in trained 
in train_save_model.py, the data used to train the model is
scraped by artist_lyric_scraper.py.
"""

import argparse
import joblib

# run python guress_singer.py --help will return help message
parser = argparse.ArgumentParser(description='It is a program to predict artist from lyrics')

# add lyric argument
parser.add_argument(
    "lyric", 
    help="Give me a lyric of either Queen or Simon & Garfunkel.", 
    type=str)

# load trained singer predictor model
model = joblib.load('artist_predictor.pkl') 

# get lyric argument
args = parser.parse_args()

# print model prediction of singer
print(model.predict([args.lyric]))

