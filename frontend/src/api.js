import axios from 'axios';

const BACKEND_URL = 'http://localhost:5000/api';
const PROXY_URL = 'http://localhost:8000/api';

export const fetchPopularMovies = async () => {
    try {
        // Popular movies still come from our ML backend (or could be moved to proxy if implemented there)
        // For now, let's keep it on backend as it uses the dataset
        const response = await axios.get(`${BACKEND_URL}/popular`);
        return response.data;
    } catch (error) {
        console.error("Error fetching popular movies:", error);
        return [];
    }
};

export const searchMovies = async (query) => {
    try {
        // Use Proxy Service for search
        const response = await axios.get(`${PROXY_URL}/search`, {
            params: { query }
        });
        return response.data;
    } catch (error) {
        console.error("Error searching movies:", error);
        return [];
    }
};

export const getRecommendations = async (title) => {
    try {
        // Recommendations still come from ML backend
        const response = await axios.get(`${BACKEND_URL}/recommend`, {
            params: { title }
        });
        return response.data;
    } catch (error) {
        console.error("Error getting recommendations:", error);
        return [];
    }
};

export const getMovie = async (movieId) => {
    try {
        // Use Proxy Service for movie details
        const response = await axios.get(`${PROXY_URL}/movie/${movieId}`);
        return response.data;
    } catch (error) {
        console.error("Error getting movie details:", error);
        return null;
    }
};

export const getPoster = async (movieId) => {
    try {
        // Use Proxy Service for poster
        // Note: Proxy returns { poster: "url" } or details with poster field
        // Let's use the movie details endpoint as it's more robust or a specific poster endpoint if we made one
        // We made /api/movie/{id} which returns 'poster' field.
        // We didn't explicitly make /api/poster/{id} in the PROXY main.py, only in the FLASK app.
        // Let's check main.py... wait, I did not add /api/poster to main.py in the previous turn.
        // I added /api/search, /api/movie/{id}, /api/recommendations/{id}.
        // So let's use getMovie to get the poster.
        const response = await axios.get(`${PROXY_URL}/movie/${movieId}`);
        return response.data.poster;
    } catch (error) {
        console.error("Error getting poster:", error);
        return null;
    }
};
