from flask import jsonify, render_template, redirect, session, request
from flask_app import app
from flask_app.models.user import User
from flask_app.models.review import Review
import requests
from unittest.mock import patch

# Mocked movie data
MOCK_POPULAR_MOVIES = {
    "items": [
        {"id": "tt1234567", "title": "Fake Movie 1", "year": "2024", "imDbRating": "8.5"},
        {"id": "tt2345678", "title": "Fake Movie 2", "year": "2023", "imDbRating": "7.9"},
        {"id": "tt3456789", "title": "Fake Movie 3", "year": "2022", "imDbRating": "9.0"},
        {"id": "tt4567890", "title": "Fake Movie 4", "year": "2021", "imDbRating": "8.1"},
        {"id": "tt5678901", "title": "Fake Movie 5", "year": "2020", "imDbRating": "7.5"},
    ]
}

MOCK_MOVIE_DETAILS = {
    "id": "tt1234567",
    "title": "Fake Movie 1",
    "plot": "This is a fake plot for testing.",
    "imDbRating": "8.5"
}

# Mock function for API requests
def mock_requests_get(url):
    print(f"Mocking request: {url}")  # Debugging print statement
    if "MostPopularMovies" in url:
        return MockResponse(MOCK_POPULAR_MOVIES)
    elif "Title" in url:
        return MockResponse(MOCK_MOVIE_DETAILS)
    return MockResponse({})

class MockResponse:
    def __init__(self, json_data, status_code=200):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')

    data = {'id': session['user_id']}
    user = User.get_by_id(data)

    if not user:
        session.clear()
        return redirect('/logout')

    with patch("requests.get", side_effect=mock_requests_get):
        movie = requests.get('https://imdb-api.com/en/API/MostPopularMovies/k_i1e26rt1')
        movies = movie.json()['items']

    return render_template('dashboard.html', user=user, movies=movies)

@app.route('/movie/<id>/details')
def show_movie(id):
    if 'user_id' not in session:
        return redirect('/logout')

    data = {'id': session['user_id']}
    user = User.get_by_id(data)

    with patch("requests.get", side_effect=mock_requests_get):
        movie = requests.get(f'https://imdb-api.com/en/API/Title/k_i1e26rt1/{id}')
        movies = movie.json()

    return render_template('movie_details.html', user=user, movies=movies)