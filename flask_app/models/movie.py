
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

