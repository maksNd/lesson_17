"""
api = Api(app)                  - регистрируем новое api
all_routes = api.namespace('')  - регистрируем общий namespace (namespace - позволяет делить приложение)
Группа адресов которая начинается с одного и того же слова и есть namespace

@all_routes.route('/books')     - регистрируем новый маршрут
class Books(Resource):
    def get(self):              - метод GET
        return[{'id':1}], 200
    def post(self):             - метод POST
        return '', 201
"""
import json

from flask import Flask, request, jsonify
from flask_restx import Resource, Api

app = Flask(__name__)

api = Api(app)
book_namespace = api.namespace('')

# данные для примера
books = {1: {"name": "Harry Potter", "year": 2000, "author": "Joan Routing"},
         2: {"name": "Monte-Cristo", "year": 1844, "author": "Alexandre Dumas"}}


@book_namespace.route('/books')  # регистрируем маршруты именно у неймспейса
class BooksView(Resource):  # класс для работы со всеми книгами
    def get(self):
        # return json.dumps(books), 200
        return books, 200

    def post(self):
        data_for_create_new = request.json
        books[len(books) + 1] = data_for_create_new
        print(books)
        return '', 201


@book_namespace.route('/books/<int:pk>')
class BookView(Resource):  # класс для работы с одной книгой
    def get(self, pk):
        return books[pk], 200

    def delete(self, pk):
        del books[pk]
        return '', 204


if __name__ == '__main__':
    app.run()
