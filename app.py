# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class MoviesSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()


class DirectorsSchema(Schema):
    id = fields.Int()
    name = fields.Str()


class GenresSchema(Schema):
    id = fields.Int()
    name = fields.Str()


api = Api(app)
api.app.config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 4}
movie_ns = api.namespace("movies")
director_ns = api.namespace("directors")
genre_ns = api.namespace("genres")


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        all_movies = Movie.query.all()
        return MoviesSchema(many=True).dump(all_movies), 200

    def post(self):
        req_json = request.json
        new_movie = Movie(**req_json)
        with db.session.begin():
            db.session.add(new_movie)
        return "", 201


@movie_ns.route("/<int:mid>")
class MovieView(Resource):
    def get(self, mid: int):
        movie = Movie.query.get(mid)
        if len(MoviesSchema().dump(movie)) > 0:
            return MoviesSchema().dump(movie), 200
        else:
            return '', 404

    def put(self, mid: int):
        movie = Movie.query.get(mid)
        if len(MoviesSchema().dump(movie)) > 0:
            req_json = request.json
            movie.title = req_json.get("title")
            movie.trailer = req_json.get("trailer")
            movie.year = req_json.get("year")
            movie.rating = req_json.get("rating")
            movie.genre_id = req_json.get("genre_id")
            movie.director_id = req_json.get("director_id")
            with db.session.begin():
                db.session.add(movie)
            return "", 204
        else:
            return '', 404

    def delete(self,mid: int):
        movie = Movie.query.get(mid)
        if len(MoviesSchema().dump(movie)) > 0:
            with db.session.begin():
                db.session.delete(movie)
            return "", 204
        else:
            return '', 404


if __name__ == '__main__':
    app.run(debug=True)
