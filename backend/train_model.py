import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import ast
import os
import scipy.sparse

def train():
    print("Loading data...")
    try:
        movies = pd.read_csv('../data/tmdb_5000_movies.csv')
        credits = pd.read_csv('../data/tmdb_5000_credits.csv')
    except FileNotFoundError:
        print("Error: Dataset files not found in ../data/")
        return

    print("Merging data...")
    movies = movies.merge(credits, on='title')

    print("Preprocessing...")
    # Check if poster_path exists, if not create it (to handle dataset variations)
    if 'poster_path' not in movies.columns:
        print("WARNING: poster_path column missing from dataset. Posters will not be displayed.")
        movies['poster_path'] = None

    # Keep relevant columns
    movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew', 'vote_average', 'vote_count', 'popularity', 'release_date', 'poster_path']]
    movies.dropna(subset=['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew', 'vote_average', 'vote_count', 'popularity'], inplace=True)

    def convert(obj):
        L = []
        for i in ast.literal_eval(obj):
            L.append(i['name'])
        return L

    def convert3(obj):
        L = []
        counter = 0
        for i in ast.literal_eval(obj):
            if counter != 3:
                L.append(i['name'])
                counter += 1
            else:
                break
        return L

    def fetch_director(obj):
        L = []
        for i in ast.literal_eval(obj):
            if i['job'] == 'Director':
                L.append(i['name'])
                break
        return L

    movies['genres'] = movies['genres'].apply(convert)
    movies['keywords'] = movies['keywords'].apply(convert)
    movies['cast'] = movies['cast'].apply(convert3)
    movies['crew'] = movies['crew'].apply(fetch_director)

    movies['genres'] = movies['genres'].apply(lambda x: [i.replace(" ", "") for i in x])
    movies['keywords'] = movies['keywords'].apply(lambda x: [i.replace(" ", "") for i in x])
    movies['cast'] = movies['cast'].apply(lambda x: [i.replace(" ", "") for i in x])
    movies['crew'] = movies['crew'].apply(lambda x: [i.replace(" ", "") for i in x])

    movies['tags'] = movies['overview'].apply(lambda x: x.split() if isinstance(x, str) else []) + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
    
    new_df = movies[['movie_id', 'title', 'tags', 'vote_average', 'vote_count', 'popularity', 'overview', 'release_date', 'poster_path']]
    # Note: Added overview and release_date to new_df for frontend display
    
    new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x).lower())

    print("Vectorizing...")
    tfidf = TfidfVectorizer(max_features=5000, stop_words='english')
    tfidf_matrix = tfidf.fit_transform(new_df['tags'])

    print("Saving models...")
    if not os.path.exists('../models'):
        os.makedirs('../models')

    pickle.dump(new_df, open('../models/movies_metadata.pkl', 'wb'))
    pickle.dump(tfidf, open('../models/tfidf_vectorizer.pkl', 'wb'))
    scipy.sparse.save_npz('../models/tfidf_matrix.npz', tfidf_matrix)

    print("Done! Artifacts saved to ../models/")

if __name__ == "__main__":
    train()
