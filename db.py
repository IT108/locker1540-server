import postgresql
import constants
import datetime
import random


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
