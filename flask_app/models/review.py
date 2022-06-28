
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user


class Review:
    def __init__(self, data):
        self.id = data['id']
        self.rating = data['rating']
        self.comment = data['comment']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.movie_id = data['movie_id']
        self.user = None


    @classmethod 
    def save(cls, data):
        query = "INSERT INTO reviews (rating, comment, user_id, movie_id) VALUES (%(rating)s, %(comment)s, %(user_id)s, %(movie_id)s);"
        return connectToMySQL('popmovie').query_db(query, data)


    @staticmethod
    def validate_reviews(data):
        is_valid = True 
        if len(data['comment']) < 10:
            flash('Comment must be a minimum of 10 characters.')
            is_valid = False
        if data['rating'] == "":
            flash('A rating needs to be given.')
            is_valid = False
        return is_valid


    @classmethod
    def get_all_reviews(cls):
        query = "SELECT * FROM reviews JOIN users ON users.id = reviews.user_id;"
        result = connectToMySQL('popmovie').query_db(query)
        list_of_reviews = []
        for row in result:
            this_review = cls(row)
            users_dictionary = {
                'id': row['users.id'],
                'username': row['username'],
                'password': row['password'],
                'email': row['email'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            associated_user = user.User(users_dictionary)
            this_review.user = associated_user
            list_of_reviews.append(this_review)
        return list_of_reviews


    @classmethod 
    def delete(cls, data):
        query = "DELETE FROM reviews where id = %(id)s;"
        return connectToMySQL('popmovie').query_db(query, data)

