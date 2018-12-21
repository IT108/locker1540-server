import postgresql
import constants
import datetime
import random
import csv


def init():
    constants.DB = postgresql.open('pq://' + constants.username + ':' + constants.password + '@' + constants.DBIP
                                   + ':5432/' + constants.DBName)


def get_card(card):
    resp = constants.DB.query('select active, greeting, position, id from public.users where card = \'' + card + '\'')
    if resp.__len__() > 0:
        if resp[0][0]:
            login_plus(str(resp[0][3]))
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


def login_plus(id):
    i = constants.DB.query('select today_login from public.users where id=' + id)
    i += 1
    constants.DB.query('update public.users set today_login=' + i + ' where id=' + id)


def update_logins():
    time = datetime.datetime.now()
    filename = "logs/" + time.day + '.' + time.month + '.' + time.year + '.log'
    i = []
    q = constants.DB.query('select id, name, today_login from public.users')
    for a in q:
        i.append([a[0], a[1], a[2]])
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(i)
    constants.DB.query('update public.users set today_login=0')
