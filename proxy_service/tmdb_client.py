import requests
import os
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = os.getenv("TMDB_BASE_URL", "https://api.themoviedb.org/3")
POSTER_BASE_URL = os.getenv("POSTER_BASE_URL", "https://image.tmdb.org/t/p/w500")
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 5))

def get_full_poster_url(poster_path):
    if poster_path:
        return f"{POSTER_BASE_URL}{poster_path}"
    return None

def get_full_backdrop_url(backdrop_path):
    if backdrop_path:
        return f"{POSTER_BASE_URL}{backdrop_path}"
    return None

def search_movies(query):
    if not TMDB_API_KEY:
        raise ValueError("TMDB_API_KEY not found in environment variables")
    
    url = f"{TMDB_BASE_URL}/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "query": query,
        "language": "en-US"
    }
    
    try:
        response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        
        results = []
        for item in data.get('results', []):
            results.append({
                "id": item['id'],
                "title": item['title'],
                "overview": item['overview'],
                "release_date": item.get('release_date'),
                "poster": get_full_poster_url(item.get('poster_path')),
                "vote_average": item.get('vote_average'),
                "vote_count": item.get('vote_count')
            })
        return results
    except requests.exceptions.Timeout:
        return {"error": "tmdb_timeout", "message": "TMDB did not respond in time"}
    except requests.exceptions.RequestException as e:
        print(f"TMDB Error: {e}")
        return {"error": "tmdb_error", "message": str(e)}

def get_movie_details(movie_id):
    if not TMDB_API_KEY:
        raise ValueError("TMDB_API_KEY not found in environment variables")
        
    url = f"{TMDB_BASE_URL}/movie/{movie_id}"
    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US"
    }
    
    try:
        response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        item = response.json()
        
        return {
            "id": item['id'],
            "title": item['title'],
            "overview": item['overview'],
            "runtime": item.get('runtime'),
            "genres": item.get('genres'),
            "release_date": item.get('release_date'),
            "homepage": item.get('homepage'),
            "poster": get_full_poster_url(item.get('poster_path')),
            "backdrop": get_full_backdrop_url(item.get('backdrop_path')),
            "vote_average": item.get('vote_average'),
            "vote_count": item.get('vote_count')
        }
    except requests.exceptions.Timeout:
        return {"error": "tmdb_timeout", "message": "TMDB did not respond in time"}
    except requests.exceptions.RequestException as e:
        print(f"TMDB Error: {e}")
        return {"error": "tmdb_error", "message": str(e)}

def get_recommendations(movie_id):
    if not TMDB_API_KEY:
        raise ValueError("TMDB_API_KEY not found in environment variables")
        
    url = f"{TMDB_BASE_URL}/movie/{movie_id}/recommendations"
    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US"
    }
    
    try:
        response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        
        results = []
        for item in data.get('results', []):
            results.append({
                "id": item['id'],
                "title": item['title'],
                "overview": item['overview'],
                "poster": get_full_poster_url(item.get('poster_path')),
                "vote_average": item.get('vote_average')
            })
        return results
    except requests.exceptions.Timeout:
        return {"error": "tmdb_timeout", "message": "TMDB did not respond in time"}
    except requests.exceptions.RequestException as e:
        print(f"TMDB Error: {e}")
        return {"error": "tmdb_error", "message": str(e)}
