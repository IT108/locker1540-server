import postgresql
import constants
import datetime
import random
from flask_login import UserMixin


class User(UserMixin):
    id = ''

    def __init__(self, id):
        self.id = id

    def get_id(self):
        return self.id

def init():
    constants.DB = postgresql.open('pq://' + constants.username + ':' + constants.password + '@' + constants.DBIP
                                   + ':5432/' + constants.DBName)


def login(card):
    resp = constants.DB.query('select admin from public.users where card = \'' + card + '\'')
    if resp.__len__() > 0:
        return str(resp[0][0])
    else:
        return False


def add_user(card, name, admin, greeting, active, position):
    values = name + ',' + card + ',' + admin + ',' + greeting + ',' + active + ',' + position
    resp = constants.DB.query('insert into public.users values (' + values + ')')
    return str(resp)


def delete_card_user(card):
    resp = constants.DB.query('delete from public.users where card = \'' + card + '\'')
    return str(resp)


def delete_name_user(name):
    resp = constants.DB.query('delete from public.users where name = \'' + name + '\'')
    return str(resp)


def get_all_users():
    resp = constants.DB.query('select * from public.users')
    need_str = ''
    for i in resp:
        for j in i:
            need_str += str(j) + '}'
        need_str += '{'
    return need_str


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
    resp = constants.DB.query("select is_authenticated, is_active, is_anonymous from public.admins where id =" + str(uid))
    user = None
    if resp.__len__() > 0:
        user = User(str(uid))

    return user


def sync():
    db_resp = constants.DB.query("select name, card, position, active from public.users")
    file = open('html/templates/table_header.txt')
    resp = file.read()
    file = open('html/templates/table_user_1.txt')
    table_user_1 = file.read()
    file = open('html/templates/table_user_2.txt')
    table_user_2 = file.read()
    file = open('html/templates/table_user_3.txt')
    table_user_3 = file.read()
    file.close()
    for i in db_resp:
        checked = 'checked'
        if not i[3]:
            checked = 'unchecked'
        resp += '\n<li class="mdl-list__item">'
        resp += '\n' + table_user_1 + '\n' + i[0] + '\n</span>'
        resp += '\n' + table_user_3 + '\n' + i[1] + '\n</span>'
        resp += '\n' + table_user_3 + '\n' + i[2] + '\n</span>'
        resp += '\n' + table_user_2 + checked + '/>\n</label>\n</span>'
        resp += '\n</li>'
    resp += '\n</ul>'
    return resp
