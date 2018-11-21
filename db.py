import postgresql
import constants
import datetime
import random
import os
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
    constants.DB = postgresql.open('pq://' + constants.username + ':' + constants.password + '@' + constants.DBIP
                                   + ':5432/' + constants.DBName)


def check_admin(admin_login, password):
    email_resp = constants.DB.query("select id from public.admins where email= '" + admin_login +
                                    "' and password = crypt('" + password + "', password)")
    login_resp = constants.DB.query("select id from public.admins where login= '" + admin_login +
                                    "' and password = crypt('" + password + "', password)")
    if email_resp.__len__() > 0:
        return email_resp[0][0]
    elif login_resp.__len__() > 0:
        return login_resp[0][0]
    return 0


def get_user(uid):
    resp = constants.DB.query(
        "select is_authenticated, is_active, is_anonymous, name from public.admins where id =" + str(uid))
    user = None
    if resp.__len__() > 0:
        user = User(str(uid), [resp[0][3]])

    return user


def make_html(example, data):
    res = str(example)
    for i in data:
        key = '{{ ' + i + ' }}'
        res = res.replace(key, data[i])
    return res


