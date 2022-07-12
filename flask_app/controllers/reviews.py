
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
    movie_data = {'imdb': id}


    movie = requests.get(f'https://imdb-api.com/en/API/Title/k_udc93q81/{id}')

    

    movies = movie.json()
    reviews = Review.get_all_reviews(movie_data)
    users = User.get_by_id(data)
    return render_template('movie_comments.html', users=users, movies=movies, reviews=reviews)


@app.route('/movie/<id>/review/create', methods=['POST'])
def create_review(id):
    if 'user_id' not in session:
        return redirect('/logout')

    if not Review.validate_reviews(request.form):
        return redirect(f'/movie/{id}/reviews') 

    data = {
            'rating': request.form['rating'],
            'comment': request.form['comment'],
            'imdb': request.form['imdb'],
            'user_id': session['user_id']
    }
    Review.save(data)
    return redirect(f'/movie/{id}/reviews')


@app.route('/delete/<id>/<int:id2>')
def delete_job(id,id2):
    data = {'id': id2}
    Review.delete(data)

    

    return redirect(f'/movie/{id}/reviews')

    
@app.route('/myreviews')
def get_my_reviews():
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        "id":session['user_id']
    }
    movie = requests.get(f'https://imdb-api.com/en/API/MostPopularMovies/k_19g8uwm0')


    movies = movie.json()['items']
    

    return render_template("reviews.html",reviews=Review.get_reviews_by_user(user_data),user=User.get_by_id(user_data),movies=movies)
