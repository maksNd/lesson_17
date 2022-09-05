"""
marshmellow - ORM framework-библиотека
Конвертирует: объект -> Json-строка,
              Json-строка -> объект
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from marshmallow import Schema, fields

app = Flask(__name__)
db = SQLAlchemy()


class User(db.Model):
    __tablenamme__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)


class UserSchema(Schema):
    """
    Создадим новую структуру данных для сериализации и десериализации структуры данных User
    """
    id = fields.Int(dump_only=True)
    'dump_only - означает, что данное поле будет использоваться только при вызове метода dump'
    name = fields.Str()
    age = fields.Int()


'Делаем dump в словарь'
user_1 = User(id=1, name='Alex', age=32)  # создадим для примера
user_2 = User(id=2, name='mk', age=18)  # создадим для примера
user_3 = User(id=3, name='Niki', age=35)
user_4 = User(id=4, name='Raf', age=26)

print()

################################ СЕРИАЛИЗАЦИЯ ################################
user_schema = UserSchema()  # создадим экземпляр (для сериализации/десериализации структуры User)
result = user_schema.dump(user_2)
print('user_schema.dump(user_2) - ', result)
print(type(result))
print(result['name'], '\n')

'Делаем dump в строку (что является json-ом)'
result = user_schema.dumps(user_3)
print('user_schema.dumps(user_3) - ', result)
print(type(result), '\n')

users_schema = UserSchema(many=True)  # создадим экземпляр (для сериализации/десериализации структуры User)
'manu=True - позволит делать множественную сериализацию'
result_many = users_schema.dump([user_1, user_2, user_3, user_4])  # сериализация (возвращает список словарей)
print(result_many)

result_many_str = users_schema.dumps([user_1, user_2, user_3, user_4])  # сериализация (возвращает строку)
print(result_many_str, '\n')

################################ ДЕСЕРИАЛИЗАЦИЯ ################################
user_json_str = '{"name": "John", "age": 35}'  # данные для десериализации

user_dict = user_schema.loads(user_json_str)  # десериализуем данные (вернет словарь)
user_from_json = User(**user_dict)  # на основе этого словаря создадим экземпляр модели User
print(user_from_json.name)
print(user_from_json.age)
