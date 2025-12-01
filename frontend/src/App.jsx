import React, { useState, useEffect } from 'react';
import { fetchPopularMovies, searchMovies, getRecommendations, getPoster } from './api';
import './App.css';

function App() {
  const [movies, setMovies] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedMovie, setSelectedMovie] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [view, setView] = useState('popular'); // 'popular', 'search', 'details'

  useEffect(() => {
    loadPopularMovies();
  }, []);

  const loadPopularMovies = async () => {
    setLoading(true);
    const data = await fetchPopularMovies();
    setMovies(data);
    setLoading(false);
    setView('popular');
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;

    setLoading(true);
    const data = await searchMovies(searchQuery);
    setMovies(data);
    setLoading(false);
    setView('search');
    setSelectedMovie(null);
  };

  const handleMovieClick = async (movie) => {
    setSelectedMovie(movie);
    setLoading(true);
    const recs = await getRecommendations(movie.title);

    // Fetch posters for recommendations if missing
    const recsWithPosters = await Promise.all(recs.map(async (rec) => {
      if (!rec.poster) {
        const posterUrl = await getPoster(rec.id);
        return { ...rec, poster: posterUrl };
      }
      return rec;
    }));

    setRecommendations(recsWithPosters);
    setLoading(false);
    setView('details');
  };

  const renderMovieCard = (movie) => {
    const posterUrl = movie.poster
      ? movie.poster
      : "/placeholder.svg";

    return (
      <div key={movie.id} className="movie-card" onClick={() => handleMovieClick(movie)}>
        <img src={posterUrl} alt={movie.title} className="movie-poster" />
        <div className="movie-info">
          <h3>{movie.title}</h3>
          <span className="rating">{movie.vote_average}</span>
        </div>
      </div>
    );
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1 onClick={loadPopularMovies} style={{ cursor: 'pointer' }}>CineMatch</h1>
        <form onSubmit={handleSearch} className="search-form">
          <input
            type="text"
            placeholder="Search movies..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          <button type="submit">Search</button>
        </form>
      </header>

      <main className="app-main">
        {loading && <div className="loading">Loading...</div>}

        {!loading && view === 'details' && selectedMovie && (
          <div className="movie-details">
            <button className="back-button" onClick={() => setView('popular')}>Back to Popular</button>
            <div className="details-content">
              <div className="details-info">
                <div className="details-header">
                  <img
                    src={selectedMovie.poster ? selectedMovie.poster : "/placeholder.svg"}
                    alt={selectedMovie.title}
                    className="details-poster"
                  />
                  <div>
                    <h2>{selectedMovie.title}</h2>
                    <p className="release-date">Release Date: {selectedMovie.release_date}</p>
                    <div className="rating-large">Rating: {selectedMovie.vote_average}/10</div>
                  </div>
                </div>
                <p className="overview">{selectedMovie.overview}</p>
              </div>
            </div>

            <div className="recommendations-section">
              <h3>Recommended Movies</h3>
              <div className="movies-grid">
                {recommendations.map(renderMovieCard)}
              </div>
            </div>
          </div>
        )}

        {!loading && (view === 'popular' || view === 'search') && (
          <>
            <h2>{view === 'popular' ? 'Popular Movies' : `Search Results for "${searchQuery}"`}</h2>
            <div className="movies-grid">
              {movies.length > 0 ? movies.map(renderMovieCard) : <p>No movies found.</p>}
            </div>
          </>
        )}
      </main>
    </div>
  );
}

export default App;
