from flask import jsonify, render_template, redirect, request
from flask_app import app
import requests

@app.route('/dashboard')
def top_ten_movies():

    # -- NEED TO ADD LOGIC TO CHECK IF USER IS LOGGED IN -- #

    # IMDb API ROUTE THAT YOU HAVE TO USE AN API KEY FOR
    # FREE PLAN ONLY ALLOWS 100 API CALLS/DAY WITH API KEY
    # RETURNS 100 MOST POPULAR MOVIES THAT CAN BE PARSED TO TOP 5 ON DASHBOARD.HTML PAGE
    movie = requests.get(f'https://imdb-api.com/en/API/MostPopularMovies/k_19g8uwm0')

    movies = movie.json()['items']
    print(movie.json()['items'])

    return render_template('dashboard.html', movies = movies)

@app.route('/movie/<id>/details')
def show_movie(id):

    # -- NEED TO ADD LOGIC TO CHECK IF USER IS LOGGED IN -- #

    # IMDb API ROUTE THAT RETURNS ONE MOVIE BASED ON ITS IMDb ID
    # PARSED OUT TITLE, PLOT, AND IMDb RATING ON DETAILS.HTML PAGE
    movie = requests.get(f'https://imdb-api.com/en/API/Title/k_19g8uwm0/{id}')
    
    movies = movie.json()
    print(movie.json()['plot'])

    return render_template('movie_details.html', movies = movies)