from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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

@book_namespace