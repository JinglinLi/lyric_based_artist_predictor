import argparse
import joblib


parser = argparse.ArgumentParser(description='It is a program to predict artist from lyrics')

parser.add_argument(
    "lyric", 
    help="Give me a lyric of either Queen or Simon & Garfunkel.", 
    type=str)


model = joblib.load('lyric.pkl') 

args = parser.parse_args()

print(model.predict([args.lyric]))

# Question/Problem : pickle/joblib saved models can be loaded in .ipynb to predict, 
# but in .py throw error no attribute lyric_cleaning for __main__

# use custom class TextCleaner.py and import it in project_v3.py, save pkl
# load pkl in guess_artist.py works!!
