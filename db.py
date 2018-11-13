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


def make_html(example, data):
    res = str(example)
    for i in data:
        key = '{{ ' + i + ' }}'
        res = res.replace(key, data[i])
    return res


def sync(order):
    db_resp = constants.DB.query("select name, card, position, active, id from public.users order by " + order)
    file = open('html/templates/table_header.html')
    resp = file.read()
    file.close()
    file = open('html/templates/table_button.html')
    table_button = file.read()
    file.close()
    file = open('html/templates/table_switch.html')
    table_switch = file.read()
    file.close()
    resp += '\n<tbody>'
    q = 0
    for i in db_resp:
        resp += '\n<tr>'
        checked = 'checked'
        if not i[3]:
            checked = ''
        resp += make_html(table_button, {'id': 'table-button-' + str(q) + '-0', 'text': i[0], 'userId': str(i[4])})
        resp += make_html(table_button, {'id': 'table-button-' + str(q) + '-1', 'text': i[1], 'userId': str(i[4])})
        resp += make_html(table_button, {'id': 'table-button-' + str(q) + '-2', 'text': i[2], 'userId': str(i[4])})
        resp += make_html(table_switch, {'UserId': str(i[4]), 'id': 'table-switch-' + str(q), 'checked': checked})
        resp += '\n</tr>'
        q += 1
    resp += '\n</tbody>\n</table>'
    return resp


def get_dialog(id):
    db_resp = constants.DB.query("select name, card, position, active from public.users where id=" + id)
    file = open('html/templates/dialog.html')
    dialog = file.read()
    file.close()
    resp = make_html(dialog, {'userId': str(id), 'name': db_resp[0][0], 'card': db_resp[0][1], 'position': db_resp[0][2]})
    return resp


def update_user(id, name, card, active, position):
    if active:
        active = 'true'
    else:
        active = 'false'
    qstr = "update public.users set name = '" + name + "', card = '" + card + "', position = '" + position\
           + "', active = " + active + " where id = " + id
    db_resp = constants.DB.query(qstr)
    print(db_resp)


def add_user(name, card, active, position):
    if active:
        active = 'true'
    else:
        active = 'false'
    qstr = "insert into public.users (name, card, active, position) values ('" + name + "', '" + card + "', " + active + ", '" + position + "')"
    db_resp = constants.DB.query(qstr)
    print(db_resp)


def toggle_user(id):
    db_resp = constants.DB.query('select active from public.users where id = ' + id)
    new_active = 'true'
    res = 'activated'
    if db_resp.__len__() > 0:
        if db_resp[0][0]:
            new_active = 'false'
            res = 'inactivated'
        db_resp = constants.DB.query("update public.users set active= " + new_active + " where id = " + id)
    else:
        res = 'error'
    return res

