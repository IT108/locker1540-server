import constants
from peewee import *
from flask_login import UserMixin


class User(UserMixin):
    id = ''
    name = ''

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def get_id(self):
        return self.id

    def set_name(self, a):
        self.name = a

    def get_name(self):
        return self.name


class BaseModel(Model):
    class Meta:
        database = constants.DB


class Users(BaseModel):
    id = IntegerField(primary_key=True)
    name = TextField()
    card = TextField()
    greeting = TextField(default='-1')
    active = BooleanField(default=True)
    position = TextField(default='teacher')


class Admins(BaseModel):
    id = IntegerField(primary_key=True)
    name = TextField()
    email = TextField()
    login = TextField()
    password = TextField()
    active = BooleanField(default=True)
    is_active = BooleanField(default=True)
    is_authenticated = BooleanField(default=False)
    is_anonymous = BooleanField(default=False)
