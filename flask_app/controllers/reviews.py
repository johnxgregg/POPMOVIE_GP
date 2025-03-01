from flask import jsonify, render_template, redirect, session, request
from flask_app import app
from flask_app.models.user import User
from flask_app.models.review import Review
import requests
from unittest.mock import patch

# Mocked movie details
MOCK_MOVIE_DETAILS = {
    "id": "tt1234567",
    "title": "Fake Movie 1",
    "plot": "This is a fake plot for testing.",
    "imDbRating": "8.5"
}

# Mock function for API requests
def mock_requests_get(url):
    print(f"Mocking request: {url}")  # Debugging print statement
    if "Title" in url:
        return MockResponse(MOCK_MOVIE_DETAILS)
    return MockResponse({})

class MockResponse:
    def __init__(self, json_data, status_code=200):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

@app.route('/movie/<id>/reviews')
def new_review(id):
    if 'user_id' not in session:
        return redirect('/logout')

    data = {'id': session['user_id']}
    movie_data = {'imdb': id}

    with patch("requests.get", side_effect=mock_requests_get):
        movie = requests.get(f'https://imdb-api.com/en/API/Title/k_i1e26rt1/{id}')
        movies = movie.json()

    reviews = Review.get_all_reviews(data)

    return render_template('movie_comments.html', users=User.get_by_id(data), movies=movies, reviews=reviews)

@app.route('/movie/<id>/review/create', methods=['POST'])
def create_review(id):
    if 'user_id' not in session:
        return redirect('/logout')

    if not Review.validate_reviews(request.form):  # Ensure validation function exists
        return redirect(f'/movie/{id}/reviews')

    data = {
        'rating': request.form['rating'],
        'comment': request.form['comment'],
        'imdb': id,
        'user_id': session['user_id']
    }

    Review.save(data)
    return redirect(f'/movie/{id}/reviews')

@app.route('/myreviews')
def my_reviews():
    if 'user_id' not in session:
        return redirect('/logout')

    data = {'id': session['user_id']}
    user = User.get_by_id(data)

    reviews = Review.get_reviews_by_user(data)  # Ensure this function exists

    return render_template('reviews.html', user=user, reviews=reviews)