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
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')

        movies = Movie.query

        if director_id:
            movies = movies.filter(Movie.director_id == director_id)
        elif genre_id:
            movies = movies.filter(Movie.genre_id == genre_id)
        movies = movies.all()
        return MoviesSchema(many=True).dump(movies), 200

    def post(self):
        req_json = request.json
        new_movie = Movie(**req_json)
        db.session.add(new_movie)
        db.session.commit()
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
            db.session.add(movie)
            db.session.commit()
            return "", 204
        else:
            return '', 404

    def delete(self, mid: int):
        movie = Movie.query.get(mid)
        if len(MoviesSchema().dump(movie)) > 0:
            db.session.delete(movie)
            db.session.commit()
            return "", 204
        else:
            return '', 404


@director_ns.route("/")
class DirectorsView(Resource):
    def get(self):
        return DirectorsSchema(many=True).dump(Director.query.all()), 200

    def post(self):
        req_json = request.json
        new_director = Director(**req_json)
        db.session.add(new_director)
        db.session.commit()
        return "", 201


@director_ns.route("/<int:did>")
class DirectorView(Resource):
    def get(self, did: int):
        director = Director.query.get(did)
        if len(DirectorsSchema().dump(director)) > 0:
            return DirectorsSchema().dump(director), 200
        else:
            return '', 404

    def put(self, did: int):
        director = Director.query.get(did)
        if len(DirectorsSchema().dump(director)) > 0:
            req_json = request.json
            director.name = req_json.get("name")
            db.session.add(director)
            db.session.commit()
            return "", 204
        else:
            return '', 404

    def delete(self, did: int):
        director = Director.query.get(did)
        if len(DirectorsSchema().dump(director)) > 0:
            db.session.delete(director)
            db.session.commit()
            return "", 204
        else:
            return '', 404


@genre_ns.route('/')
class GenresView(Resource):
    def get(self):
        return GenresSchema(many=True).dump(Genre.query.all()), 200

    def post(self):
        req_json = request.json
        new_genre = Genre(**req_json)
        db.session.add(new_genre)
        db.session.commit()
        return "", 201


@genre_ns.route("/<int:gid>")
class GenreView(Resource):
    def get(self, gid: int):
        genre = Genre.query.get(gid)
        if len(GenresSchema().dump(genre)) > 0:
            return GenresSchema().dump(genre), 200
        else:
            return '', 404

    def put(self, gid: int):
        genre = Genre.query.get(gid)
        if len(GenresSchema().dump(genre)) > 0:
            req_json = request.json
            genre.name = req_json.get("name")
            db.session.add(genre)
            db.session.commit()
            return "", 204
        else:
            return '', 404

    def delete(self, gid: int):
        genre = Genre.query.get(gid)
        if len(GenresSchema().dump(genre)) > 0:
            db.session.delete(genre)
            db.session.commit()
            return "", 204
        else:
            return '', 404


if __name__ == '__main__':
    app.run(debug=True)
