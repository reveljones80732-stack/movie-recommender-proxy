import pandas as pd
try:
    df = pd.read_csv('../data/tmdb_5000_movies.csv')
    print("CSV Columns:", df.columns.tolist())
    if 'poster_path' in df.columns:
        print("poster_path exists.")
    else:
        print("poster_path MISSING.")
except Exception as e:
    print(e)
