
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user


class Review:
    def __init__(self, data):
        self.id = data['id']
        self.rating = data['rating']
        self.comment = data['comment']
        self.imdb = data['imdb']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None


    @classmethod 
    def save(cls, data):
        query = "INSERT INTO reviews (rating, comment, imdb, user_id) VALUES (%(rating)s, %(comment)s, %(imdb)s, %(user_id)s);"
        return connectToMySQL('popmovie').query_db(query, data)


    @staticmethod
    def validate_reviews(data):
        is_valid = True 
        if len(data['comment']) < 1:
            flash('Comment cannot be left blank!')
            is_valid = False
        if len(data['rating']) > 1 :
            flash('A rating needs to be given!')
            is_valid = False
        return is_valid


    @classmethod
    def get_all_reviews(cls, data):
        query = "SELECT *, reviews.user_id AS reviewer FROM reviews "\
            "JOIN users ON users.id = reviews.user_id "\
            "WHERE reviews.imdb = %(imdb)s;"
    
        result = connectToMySQL('popmovie').query_db(query, data)

    # Ensure result is always a list
        if not result:
            return []  # Return an empty list instead of False or None
        print (result)
        return result  # Return actual query results


    @classmethod 
    def delete(cls, data):
        query = "DELETE FROM reviews where id = %(id)s;"
        return connectToMySQL('popmovie').query_db(query, data)

    @classmethod
    def get_reviews_by_user(cls, data):
        query = "SELECT * FROM reviews WHERE user_id = %(id)s;"
        results = connectToMySQL('popmovie').query_db(query, data)
        reviews = []
        if not results:
            return reviews
        for row in results:
            reviews.append(cls(row))
        return reviews

