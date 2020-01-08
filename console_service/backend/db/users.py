from backend.db.models import *
import backend.db.common as common


def get_all_users(order):
    order = common.translate_column_names('Users', order)
    db_resp = Users.select().order_by(order).dicts()
    return db_resp


def get_user_by_id(id):
    db_resp = Users.select().where(Users.id == id).dicts()
    return db_resp[0]


def update_user(id, name, card, active, position):
    query = Users.update(name=name, card=str(card).upper(), position=position, active=active).where(Users.id == id)
    db_resp = query.execute()
    print(db_resp)
    return db_resp


def create_user(name, card, active, position):
    user = Users(name=name, card=card, position=position, active=active)
    db_resp = user.save()
    print(db_resp)
    return db_resp


def toggle_user_state(id):
    user = Users[id]
    state = not user.active
    res = ('inactivated', 'activated')[state]
    user.active = state
    db_resp = user.save()
    print(db_resp)
    return res
