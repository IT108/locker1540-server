import constants
import os
from backend.db import path, make_html


def sync(order):
    db_resp = constants.DB.query("select login, name, email, id from public.admins order by " + order)
    file = open(os.path.join(path, 'html/templates/admins/table_header.html'))
    resp = file.read()
    file.close()
    file = open(os.path.join(path, 'html/templates/admins/table_button.html'))
    table_button = file.read()
    file.close()
    file = open(os.path.join(path, 'html/templates/admins/table_switch.html'))
    table_switch = file.read()
    file.close()
    resp += '\n<tbody>'
    q = 0
    for i in db_resp:
        resp += make_html(table_button, {'id': 'table-button-' + str(q) + '-0', 'text': i[0], 'userId': str(i[3])})
        resp += make_html(table_button, {'id': 'table-button-' + str(q) + '-1', 'text': i[1], 'userId': str(i[3])})
        resp += make_html(table_button, {'id': 'table-button-' + str(q) + '-1', 'text': i[2], 'userId': str(i[3])})
        resp += '\n</tr>'
        q += 1
    resp += '\n</tbody>\n</table>'
    return resp


def get_dialog(id):
    db_resp = constants.DB.query("select name, email, login from public.admins where id=" + id)
    file = open(os.path.join(path, 'html/templates/admins/dialog.html'))
    dialog = file.read()
    file.close()
    resp = make_html(dialog,
                     {'deleteF': "deleteUser(" + str(id) + ");", 'error': "", 'onClick': "updateUser(" + str(id) + ");", 'name': db_resp[0][0],
                      'email': db_resp[0][1], 'login': db_resp[0][2]})
    return resp


def get_empty_dialog():
    file = open(os.path.join(path, 'html/templates/admins/add_dialog.html'))
    dialog = file.read()
    file.close()
    resp = make_html(dialog,
                     {'error': "", 'onClick': "addUser();"})
    return resp


def update_user(id, name, email, login):
    old_login = constants.DB.query("select login from public.admins where id=" + id)[0][0]
    if check_login(login) and old_login != login:
        return 'NO'
    qstr = "update public.admins set name = '" + name + "', email = '" + email + "', login = '" + login + "' where " \
                                                                                                          "id = " + id
    db_resp = constants.DB.query(qstr)
    print(db_resp)
    return 'OK'


def add_user(name, email, login, password):
    if check_login(login):
        return 'NO'
    qstr = "insert into public.admins (name, email, login, password) values ('" + name + "', '" + email + \
           "', '" + login + "', crypt('" + password + "',gen_salt('bf')))"
    db_resp = constants.DB.query(qstr)
    print(db_resp)
    return 'OK'


def check_login(login):
    db_resp = constants.DB.query("select * from public.admins where login='" + login + "'")
    if db_resp.__len__() > 0:
        return True
    return False


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


def delete_admin(id):
    qstr = "DELETE FROM public.admins WHERE id=" + id
    constants.DB.query(qstr)
