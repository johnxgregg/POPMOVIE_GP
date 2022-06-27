from flask import jsonify, render_template, redirect, session, request
from flask_app import app
from flask_app.models.user import User
from flask_app.models.movie import Review
import requests

@app.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    # IMDb API ROUTE THAT YOU HAVE TO USE AN API KEY FOR
    # FREE PLAN ONLY ALLOWS 100 API CALLS/DAY WITH API KEY
    # RETURNS 100 MOST POPULAR MOVIES THAT CAN BE PARSED TO TOP 5 ON DASHBOARD.HTML PAGE
    movie = requests.get(f'https://imdb-api.com/en/API/MostPopularMovies/k_19g8uwm0')

    movies = movie.json()['items']
    print(movie.json()['items'])
    user=User.get_by_id(data)

    return render_template('dashboard.html', user = user, movies = movies)

@app.route('/movie/<id>/details')
def show_movie(id):

    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    # IMDb API ROUTE THAT RETURNS ONE MOVIE BASED ON ITS IMDb ID
    # PARSED OUT TITLE, PLOT, AND IMDb RATING ON DETAILS.HTML PAGE
    movie = requests.get(f'https://imdb-api.com/en/API/Title/k_19g8uwm0/{id}')
    
    movies = movie.json()
    print(movie.json()['plot'])
    user=User.get_by_id(data)

    return render_template('movie_details.html', user = user, movies = movies)


@app.route('/movies/<id>/reviews')
def new_review(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {'id': session['user_id']}
    movie = requests.get(f'https://imdb-api.com/en/API/Title/k_19g8uwm0/{id}')
    movies = movie.json()
    return render_template('movie_comments.html', users=User.get_by_id(data), movies=movies)

@app.route('/create', methods=['POST'])
def create_review():
    if 'user_id' not in session:
        return redirect('/logout')

        # Possible validations?
    #if not Movie.validate_comments(request.form):
        #return redirect('/movies/comments') 

    data = {
            'rating': request.form['rating'],
            'comment': request.form['comment'],
            'user_id': session['user_id']
    }
    Review.save(data)
    return redirect('/movies/<id>/reviews')