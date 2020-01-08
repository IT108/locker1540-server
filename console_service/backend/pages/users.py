from backend.db.users import *
from flask import render_template


def sync(order):
    users = get_all_users(order)
    resp = render_template('users/users_table.html', users=users)
    return resp


def get_dialog(id):
    db_resp = get_user_by_id(id)
    return render_template('users/dialog.html', **db_resp)


def update_data(id, name, card, active, position):
    update_user(id, name, card, active, position)


def add_user(name, card, active, position):
    create_user(name, str(card).upper(), active, position)


def toggle_user(id):
    return toggle_user_state(id)

