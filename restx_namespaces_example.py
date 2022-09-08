from flask import Flask, request
from flask_restx import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema

app = Flask(__name__)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

api = Api(app)
book_namespace = api.namespace('books')
author_namespace = api.namespace('authors')


class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    year = db.Column(db.Integer)


class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=True)
    last_name = db.Column(db.String, nullable=True)


class BookSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    year = fields.Int()


class AuthorSchema(Schema):
    id = fields.Int()
    first_name = fields.Str()
    last_name = fields.Str()


book_schema = BookSchema()
books_schema = BookSchema(many=True)

author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)

book_1 = Book(name="Harry Potter", year=2000)
book_2 = Book(name="Monte-Cristo", year=1844)

author_1 = Author(first_name='Joan', last_name='Stewart')
author_2 = Author(first_name='Alexandre', last_name='Dumas')

db.create_all()
with db.session.begin():
    db.session.add_all([book_1, book_2])
    db.session.add_all([author_1, author_2])


@book_namespace.route('/')
class BooksView(Resource):
    def get(self):
        all_books = db.session.query(Book).all()
        return books_schema.dump(all_books), 200

    def post(self):
        requested_json = request.json
        new_book = Book(**requested_json)

        with db.session.begin():
            db.session.add(new_book)

        return '', 201


@book_namespace.route('/<int:pk>')
class BookView(Resource):
    def get(self, pk):
        try:
            book = db.session.query(Book).filter(Book.id == pk).one()
            return book_schema.dump(book), 200
        except Exception:
            return '', 404

    def put(self, pk):
        book = db.session.query(Book).get(pk)
        requested_json = request.json
        book.name = requested_json.get('name')
        book.year = requested_json.get('year')

        db.session.add(book)
        db.session.commit()

        return '', 204

    def patch(self, pk):
        book = db.session.query(Book).get(pk)
        requested_json = request.json
        if 'name' in requested_json:
            book.name = requested_json.get('name')
        if 'year' in requested_json:
            book.year = requested_json.get('year')

        db.session.add(book)
        db.session.commit()

        return '', 204


@author_namespace.route('/')
class AuthorsView(Resource):
    def get(self):
        all_authors = db.session.query(Author).all()
        print(all_authors)
        return authors_schema.dump(all_authors), 200

    def post(self):
        requested_json = request.json
        new_author = Author(**requested_json)

        with db.session.begin():
            db.session.add(new_author)

        return '', 201


@author_namespace.route('/<int:pk>')
class AuthorView(Resource):
    def get(self, pk):
        try:
            author = db.session.query(Author).filter(Author.id == pk).one()
            return author_schema.dump(author), 200
        except Exception:
            return '', 404

    def put(self, pk):
        author = db.session.query(Author).get(pk)
        requested_json = request.json
        author.first_name = requested_json.get('first_name')
        author.last_name = requested_json.get('last_name')

        db.session.add(author)
        db.session.commit()

        return '', 204

    def patch(self, pk):
        author = db.session.query(Author).get(pk)
        requested_json = request.json
        if 'first_name' in requested_json:
            author.first_name = requested_json.get('first_name')
        if 'last_name' in requested_json:
            author.last_name = requested_json.get('last_name')

        db.session.add(author)
        db.session.commit()

        return '', 204


if __name__ == '__main__':
    app.run()
