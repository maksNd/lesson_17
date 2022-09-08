from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
db = SQLAlchemy(app)


class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    author = db.Column(db.String(100))
    year = db.Column(db.Integer)


book_1 = Book(name="Harry Potter", year=2000, author="Joan Routing")
book_2 = Book(name="Monte-Cristo", year=1844, author="Alexandre Dumas")

db.create_all()
with db.session.begin():
    db.session.add_all([book_1, book_2])


class BookSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    author = fields.Str()
    year = fields.Int()


book_schema = BookSchema()  # для сериализации/десериализации одного объекта
books_schema = BookSchema(many=True)  # для сериализации/десериализации множественных объектов

api = Api(app)
book_namespace = api.namespace('')


@book_namespace.route('/books')
class BooksView(Resource):
    def get(self):
        all_books = db.session.query(Book).all()
        return books_schema.dump(all_books), 200

    def post(self):
        requested_json = request.json
        new_user = Book(**requested_json)
        with db.session.begin():
            db.session.add(new_user)
        return '', 201


@book_namespace.route('/books/<int:pk>')
class BookView(Resource):
    def get(self, pk: int):
        try:
            book = db.session.query(Book).filter(Book.id == pk).one()
            return book_schema.dump(book), 200
        except Exception as error:
            return str(error), 404

    def put(self, pk: int):  # обновление данных
        book = db.session.query(Book).get(pk)
        requested_json = request.json
        print(requested_json)

        book.name = requested_json.get('name')
        book.year = requested_json.get('year')
        book.author = requested_json.get('author')

        db.session.add(book)
        db.session.commit()

        return '', 204

    def patch(self, pk: int):  # частичное обновление данных
        book = db.session.query(Book).get(pk)
        requested_json = request.json

        if 'name' in requested_json:
            book.name = requested_json.get('name')
        if 'year' in requested_json:
            book.year = requested_json.get('year')
        if 'author' in requested_json:
            book.author = requested_json.get('author')

        db.session.add(book)
        db.session.commit()

        return '', 204

    def delete(self, pk: int):
        user = db.session.query(Book).get(pk)

        db.session.delete(user)
        db.session.commit()

        return '', 204


if __name__ == '__main__':
    app.run()
