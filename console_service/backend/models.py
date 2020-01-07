import constants
from peewee import *


class BaseModel(Model):
    class Meta:
        database = constants.DB


class Users(BaseModel):
    id = IntegerField()
    name = TextField()
    card = TextField()
    greeting = TextField()
    active = BooleanField()
    position = TextField()


class Admins(BaseModel):
    id = IntegerField()
    name = TextField()
    email = TextField()
    login = TextField()
    password = TextField()
    active = BooleanField()
    is_active = BooleanField()
    is_authenticated = BooleanField()
    is_anonymous = BooleanField()