from playhouse.pool import PooledPostgresqlExtDatabase

from backend.db.models import *

path = constants.current_path
tables = {'Users': {
    'name': Users.name,
    'card': Users.card,
    'active': Users.active,
    'position': Users.position,
    'id': Users.id,
    'greeting': Users.greeting
},
    'Admins': {
        'name': Admins.name,
        'email': Admins.email,
        'login': Admins.login,
        'password': Admins.password,
        'active': Admins.active,
        'id': Admins.id,
        'is_active': Admins.is_active,
        'is_authenticated': Admins.is_authenticated,
        'is_anonymous': Admins.is_anonymous
    }}


def init():
    constants.DB = PooledPostgresqlExtDatabase(**constants.DB_SETTINGS, **constants.PEEWEE_SETTINGS)
    constants.DB.bind([Users, Admins])
    constants.DB.connect()


def make_html(example, data):
    res = str(example)
    for i in data:
        key = '{{ ' + i + ' }}'
        res = res.replace(key, data[i])
    return res


def translate_column_names(table, column):
    res = tables.get(table, IndexError("Table not found in common"))
    if res is IndexError:
        raise res
    res = res.get(column, IndexError("Column not found in common"))
    if res is IndexError:
        raise res
    return res
