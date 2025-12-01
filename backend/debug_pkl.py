import pandas as pd
import pickle

try:
    df = pickle.load(open('../models/movies_metadata.pkl', 'rb'))
    print("Columns:", df.columns)
    print("First 5 rows poster_path:")
    print(df['poster_path'].head())
    print("Null count:", df['poster_path'].isnull().sum())
except Exception as e:
    print(e)
