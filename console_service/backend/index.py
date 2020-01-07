import constants
import os
from backend.db import path, make_html


def sync(order):
    db_resp = constants.DB.query("select name, card, position, active, id from public.users order by " + order)
    file = open(os.path.join(path, 'html/templates/index/table_header.html'))
    resp = file.read()
    file.close()
    file = open(os.path.join(path, 'html/templates/index/table_button.html'))
    table_button = file.read()
    file.close()
    file = open(os.path.join(path, 'html/templates/index/table_switch.html'))
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
    file = open(os.path.join(path, 'html/templates/index/dialog.html'))
    dialog = file.read()
    file.close()
    resp = make_html(dialog,
                     {'userId': str(id), 'name': db_resp[0][0], 'card': db_resp[0][1],
                      db_resp[0][2] + 'Checked': 'checked'})
    return resp


def update_user(id, name, card, active, position):
    if active:
        active = 'true'
    else:
        active = 'false'
    qstr = "update public.users set name = '" + name + "', card = '" + str(card).upper() + "', position = '" + position \
           + "', active = " + active + " where id = " + id
    db_resp = constants.DB.query(qstr)
    print(db_resp)


def add_user(name, card, active, position):
    if active:
        active = 'true'
    else:
        active = 'false'
    qstr = "insert into public.users (name, card, active, position) values ('" + name + "', '" + str(card).upper() + "', " + active + ", '" + position + "')"
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
