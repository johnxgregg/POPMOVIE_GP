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
        self.user = None

    @classmethod 
    def save(cls, data):
        query = "INSERT INTO reviews (rating, comment, user_id) VALUES (%(rating)s, %(comment)s, %(user_id)s);"
        return connectToMySQL('popmovie').query_db(query, data)


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM reviews JOIN users on reviews.user_id=users.id;"
        results =  connectToMySQL('popmovie').query_db(query)
        all_reviews = []
        for row in results:
            movie = cls(row)
            user_data = {
                "id":row["users.id"],
                "first_name":row["first_name"],
                "last_name":row["last_name"],
                "email":row["email"],
                "password":row["password"],
                "created_at":row["users.created_at"],
                "updated_at":row["users.updated_at"],

            }
            movie.user = user.User(user_data)
            all_reviews.append(movie)
        return all_reviews

    @staticmethod
    def validate_review(movie):
        is_valid = True
        if len(movie['comment']) < 2:
            is_valid = False
            flash("Comment must be at least 2 characters","movie")
        return is_valid

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM reviews JOIN users ON reviews.user_id=users.id WHERE reviews.id = %(id)s;"
        results = connectToMySQL('popmovie').query_db(query,data)
        if len(results) < 1:
            return False
        row = results[0]
        movie = cls(row)
        user_data = {
                "id":row["users.id"],
                "first_name":row["first_name"],
                "last_name":row["last_name"],
                "email":row["email"],
                "password":row["password"],
                "created_at":row["users.created_at"],
                "updated_at":row["users.updated_at"],
            }
        movie.user = user.User(user_data)
        return movie

    @classmethod
    def update(cls, data):
        query = "UPDATE reviews SET comment=%(comment)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL('popmovie').query_db(query,data)
        
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM reviews WHERE id = %(id)s;"
        return connectToMySQL('popmovie').query_db(query,data)
