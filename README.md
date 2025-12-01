# Movie Recommender System

A complete Movie Recommender System Website using Machine Learning (Content-Based Filtering) and the Kaggle TMDB 5000 Movie Dataset.

## Features
- **Machine Learning**: TF-IDF Vectorization & Cosine Similarity.
- **Backend**: Flask API serving recommendations and movie data.
- **Frontend**: React-based modern UI with dark mode.
- **Data**: TMDB 5000 Movie Dataset.

## Prerequisites
- Python 3.8+
- Node.js & npm

## Setup Instructions

### 1. Dataset
Download the TMDB 5000 Movie Dataset from Kaggle and place the following files in `movie-recommender/data/`:
- `tmdb_5000_movies.csv`
- `tmdb_5000_credits.csv`

### 2. Backend & Model Training
Navigate to the `backend` directory:
```bash
cd backend
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Train the model (this will generate artifacts in `models/`):
```bash
python train_model.py
```

Start the Flask API:
```bash
python app.py
```
The API will run at `http://localhost:5000`.

### 3. Frontend
Navigate to the `frontend` directory:
```bash
cd frontend
```

Install dependencies:
```bash
npm install
```

Start the React app:
```bash
npm start
```
The app will run at `http://localhost:3000`.

## API Endpoints
- `GET /api/health`: Check if API is running.
- `GET /api/popular`: Get a list of popular movies.
- `GET /api/search?query=<title>`: Search for movies.
- `GET /api/recommend?title=<title>&n=10`: Get recommendations.

## Project Structure
```
movie-recommender/
  data/          # CSV datasets
  models/        # Saved ML models
  backend/       # Flask API & Training script
  frontend/      # React App
  notebooks/     # Jupyter Notebooks
```
