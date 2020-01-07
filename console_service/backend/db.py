from peewee import *
from playhouse.pool import PooledPostgresqlExtDatabase

import constants
from backend.models import Users, Admins
from flask_login import UserMixin

path = constants.current_path


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


def init():
    constants.DB = PooledPostgresqlExtDatabase(**constants.DB_SETTINGS, **constants.PEEWEE_SETTINGS)
    constants.DB.bind([Users, Admins])
    constants.DB.connect()


def check_admin(admin_login, password):
    email_resp = constants.DB.execute_sql(
        "select id from public.admins where email= %s and password = crypt(%s, password)", (admin_login, password,))
    login_resp = constants.DB.execute_sql(
        "select id from public.admins where login=%s and password = crypt(%s, password)", (admin_login, password,))
    email_resp = email_resp.fetchone()
    login_resp = login_resp.fetchone()
    resp = 0
    if login_resp:
        resp = login_resp[0]
    if email_resp:
        resp = email_resp[0]
    return resp


def get_user(uid):
    try:
        resp = Admins[uid].name
    except Exception:
        return None
    return User(str(uid), [resp])


def make_html(example, data):
    res = str(example)
    for i in data:
        key = '{{ ' + i + ' }}'
        res = res.replace(key, data[i])
    return res
