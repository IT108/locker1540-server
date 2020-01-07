import postgresql
from console_service import constants
import datetime
import random


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
    resp = constants.DB.query('select greeting, position, id from public.users where card = \'' + card + '\'')
    if resp.__len__() > 0:
        login_plus(str(resp[0][2]))
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
    i = constants.DB.query('select today_login, name from public.users where id=' + id)
    name = i[0][1]
    i = i[0][0] + 1
    constants.DB.query('update public.users set today_login=' + str(i) + ' where id=' + id)
    write_to_log(name, id)


def write_to_log(name, id):
    time = datetime.datetime.now()
    filename = "/var/www/locker/server/static/logs/" + str(time.day) + '.' + str(time.month) + '.' + str(
        time.year) + 'full.log'
    file = open(filename, 'a')
    now = '[' + str(time.day) + '.' + str(time.month) + '.' + str(time.year) + '; ' + get_time(time.hour, time.minute, time.second) + ']'
    file.write(now + ': id=' + str(id) + '; ' + str(name) + '\r\n')
    file.close()


def get_time(hour, minute, second):
    time = normalize_num(hour) + ':' + normalize_num(minute) + ':' + normalize_num(second)
    return time


def normalize_num(number):
    if number // 10 == 0: number = '0' + str(number)
    return str(number)
