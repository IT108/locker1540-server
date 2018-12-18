import postgresql
import constants
import datetime
import random


def init():
    constants.DB = postgresql.open('pq://' + constants.username + ':' + constants.password + '@' + constants.DBIP
                                   + ':5432/' + constants.DBName)


def get_card(card):
    resp = constants.DB.query('select active, greeting, position from public.users where card = \'' + card + '\'')
    if resp.__len__() > 0:
        return str(resp[0][0]) + ';' + str(get_common_greet(resp[0][2])) + ';' + str(resp[0][1]) + ';'
    else:
        return False


def get_greet(card):
    resp = constants.DB.query('select greeting, position from public.users where card = \'' + card + '\'')
    if resp.__len__() > 0:
        return str(get_common_greet(resp[0][1])) + ';' + str(resp[0][0]) + ';'
    else:
        return -1


def get_common_greet(group):
    morning = constants.teachers_morning
    evening = constants.teachers_evening
    day = constants.teachers_day
    sequence = []
    time = datetime.datetime.now()
    if group == 'students':
        morning = constants.students_morning
        evening = constants.students_evening
        day = constants.students_day
    if 10 > time.hour > 1:
        sequence = morning
    elif 19 > time.hour > 9:
        sequence = day
    else:
        sequence = evening
    return random.choice(sequence)


def sync():
    res = ''
    resp = constants.DB.query('select card from public.users')
    for a in resp:
        res += ';'
        res += str(a[0])
    res += ';'
    return res
