from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import linear_kernel
import scipy.sparse
import os

app = Flask(__name__)
CORS(app)

# Load models
print("Loading models...")
try:
    movies_df = pickle.load(open('../models/movies_metadata.pkl', 'rb'))
    tfidf_matrix = scipy.sparse.load_npz('../models/tfidf_matrix.npz')
    # We don't necessarily need the vectorizer for inference if we only recommend based on existing movies
    # tfidf = pickle.load(open('../models/tfidf_vectorizer.pkl', 'rb'))
    
    # Compute cosine similarity matrix
    # Note: In a real production app with 5000 movies, computing this 5000x5000 matrix in memory is okay (~200MB).
    # For larger datasets, we'd use approximate nearest neighbors.
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    
    # Create indices for faster lookup
    indices = pd.Series(movies_df.index, index=movies_df['title']).drop_duplicates()
    
    print("Models loaded successfully.")
except FileNotFoundError:
    print("WARNING: Models not found. Please run train_model.py first.")
    movies_df = None
    cosine_sim = None
    indices = None

def movie_to_dict(row):
    poster_path = row.get("poster_path")
    if poster_path and isinstance(poster_path, str):
        poster_url = f"https://image.tmdb.org/t/p/w300{poster_path}"
    else:
        poster_url = None

    return {
        "id": int(row["movie_id"]),
        "title": row["title"],
        "overview": row.get("overview", ""),
        "poster": poster_url,
        "vote_average": float(row.get("vote_average", 0.0)),
        "vote_count": int(row.get("vote_count", 0) or 0),
        "popularity": float(row.get("popularity", 0.0)),
        "release_date": row.get("release_date", "")
    }

import requests

TMDB_API_KEY = "a601c2c4e22d060429173732aaf060b5"
TMDB_BASE_URL = "https://api.themoviedb.org/3"
POSTER_BASE_URL = "https://image.tmdb.org/t/p/w500"

def get_tmdb_poster_url(poster_path):
    if poster_path:
        return f"{POSTER_BASE_URL}{poster_path}"
    return None

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "models_loaded": movies_df is not None})

@app.route('/api/popular', methods=['GET'])
def get_popular():
    if movies_df is None:
        return jsonify({"error": "Models not loaded"}), 500
    
    # Return top 20 popular movies
    popular = movies_df.sort_values('popularity', ascending=False).head(20)
    results = [movie_to_dict(row) for _, row in popular.iterrows()]
    return jsonify(results)

@app.route('/api/search', methods=['GET'])
def search_movies():
    query = request.args.get('query', '')
    if not query:
        return jsonify([])
    
    try:
        response = requests.get(f"{TMDB_BASE_URL}/search/movie", params={"api_key": TMDB_API_KEY, "query": query})
        response.raise_for_status()
        data = response.json()
        
        results = []
        for item in data.get('results', []):
            results.append({
                "id": item['id'],
                "title": item['title'],
                "overview": item['overview'],
                "popularity": item['popularity'],
                "poster": get_tmdb_poster_url(item.get('poster_path')),
                "vote_average": item.get('vote_average'),
                "release_date": item.get('release_date')
            })
        return jsonify(results)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching from TMDB: {e}")
        return jsonify({"error": "Failed to fetch data from TMDB"}), 500

@app.route('/api/movie/<int:movie_id>', methods=['GET'])
def get_movie_details(movie_id):
    try:
        response = requests.get(f"{TMDB_BASE_URL}/movie/{movie_id}", params={"api_key": TMDB_API_KEY})
        if response.status_code == 404:
            return jsonify({"error": "Movie not found"}), 404
        response.raise_for_status()
        item = response.json()
        
        result = {
            "id": item['id'],
            "title": item['title'],
            "overview": item['overview'],
            "popularity": item['popularity'],
            "poster": get_tmdb_poster_url(item.get('poster_path')),
            "vote_average": item.get('vote_average'),
            "release_date": item.get('release_date')
        }
        return jsonify(result)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching from TMDB: {e}")
        return jsonify({"error": "Failed to fetch data from TMDB"}), 500

@app.route('/api/poster/<int:movie_id>', methods=['GET'])
def get_movie_poster(movie_id):
    try:
        response = requests.get(f"{TMDB_BASE_URL}/movie/{movie_id}", params={"api_key": TMDB_API_KEY})
        if response.status_code == 404:
            return jsonify({"error": "Movie not found"}), 404
        response.raise_for_status()
        item = response.json()
        
        poster_url = get_tmdb_poster_url(item.get('poster_path'))
        return jsonify({"poster": poster_url})
    except requests.exceptions.RequestException as e:
        print(f"Error fetching from TMDB: {e}")
        return jsonify({"error": "Failed to fetch data from TMDB"}), 500

@app.route('/api/recommend', methods=['GET'])
def recommend():
    if movies_df is None:
        return jsonify({"error": "Models not loaded"}), 500
    
    title = request.args.get('title', '')
    n = int(request.args.get('n', 10))
    
    if title not in indices:
        return jsonify({"error": "Movie not found"}), 404
    
    idx = indices[title]
    
    # Get similarity scores
    sim_scores = list(enumerate(cosine_sim[idx]))
    
    # Sort by similarity
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Get top n (excluding self)
    sim_scores = sim_scores[1:n+1]
    
    movie_indices = [i[0] for i in sim_scores]
    
    recommendations = movies_df.iloc[movie_indices]
    results = [movie_to_dict(row) for _, row in recommendations.iterrows()]
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
