from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List, Dict, Any, Union
import tmdb_client
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="TMDB Proxy Service")

# CORS Configuration
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:5000",
    "*" # Allow all for development convenience, restrict in production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

@app.get("/api/search")
def search(query: str = Query(..., min_length=1)):
    result = tmdb_client.search_movies(query)
    if isinstance(result, dict) and "error" in result:
        status_code = 504 if result["error"] == "tmdb_timeout" else 500
        raise HTTPException(status_code=status_code, detail=result)
    return result

@app.get("/api/movie/{movie_id}")
def get_movie(movie_id: int):
    result = tmdb_client.get_movie_details(movie_id)
    if isinstance(result, dict) and "error" in result:
        status_code = 504 if result["error"] == "tmdb_timeout" else 500
        raise HTTPException(status_code=status_code, detail=result)
    return result

@app.get("/api/recommendations/{movie_id}")
def get_recommendations(movie_id: int):
    result = tmdb_client.get_recommendations(movie_id)
    if isinstance(result, dict) and "error" in result:
        status_code = 504 if result["error"] == "tmdb_timeout" else 500
        raise HTTPException(status_code=status_code, detail=result)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
