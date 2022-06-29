
from flask import jsonify, render_template, redirect, session, request
from flask_app import app
from flask_app.models.user import User
from flask_app.models.review import Review
import requests


@app.route('/movie/<id>/reviews')
def new_review(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {'id': session['user_id']}

    movie = requests.get(f'https://imdb-api.com/en/API/Title/k_gj08scd0/{id}')
    movies = movie.json()
    reviews = Review.get_all_reviews()

    return render_template('movie_comments.html', users=User.get_by_id(data), movies=movies, reviews=reviews)


@app.route('/movie/<id>/review/create', methods=['POST'])
def create_review(id):
    if 'user_id' not in session:
        return redirect('/logout')

    if not Review.validate_reviews(request.form):
        return redirect('/movies/<id>/reviews') 

    data = {
            'rating': request.form['rating'],
            'comment': request.form['comment'],
            'imdb': request.form['imdb'],
            'user_id': session['user_id']
    }
    Review.save(data)
    return redirect(f'/movie/{id}/reviews')


@app.route('/delete/<int:id>')
def delete_job(id):
    data = {'id': id}
    Review.delete(data)
    return redirect('/movies/<id>/reviews')
    