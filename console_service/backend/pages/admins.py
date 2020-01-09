from backend.db.admins import *
from flask import render_template


def sync(order):
    db_resp = get_all_admins(order)
    return render_template('admins/admins_table.html', admins=db_resp)


def get_dialog(id):
    db_resp = get_admin_by_id(id)
    return render_template('admins/dialog.html', **db_resp)


def get_empty_dialog():
    return render_template('admins/add_dialog.html')


def update_admin(id, name, email, login):
    old_login = get_admin_by_id(id)['login']
    if check_admin_login(login) and old_login != login:
        return 'NO'
    update(id, name, email, login)
    return 'OK'


def add_user(name, email, login, password):
    if check_admin_login(login):
        return 'NO'
    create_admin(name, email, login, password)
    return 'OK'


def toggle_user(id):
    res = toggle_admin(id)
    return res


def delete_admin(id):
    remove_admin(id)
