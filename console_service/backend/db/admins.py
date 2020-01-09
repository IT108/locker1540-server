from backend.db.models import *
import backend.db.common as common


def get_all_admins(order):
    order = common.translate_column_names('Admins', order)
    db_resp = Admins.select().order_by(order).dicts()
    return db_resp


def get_admin_by_id(id):
    db_resp = Admins.select().where(Admins.id == id).dicts()
    return db_resp[0]


def update(id, name, email, login):
    query = Admins.update(name=name, login=login, email=email).where(Admins.id == id)
    db_resp = query.execute()
    print(db_resp)
    return db_resp


def check_admin_login(login):
    db_resp = Admins.select().where(Admins.login == login).count()
    res = (True, False)[db_resp == 0]
    return res


def create_admin(name, email, login, password):
    query = constants.DB.execute_sql(
        "INSERT INTO public.admins (name, email, login, password) values (%s, %s, %s, crypt(%s, gen_salt('bf')))",
        (name, email, login, password,))
    return query


def toggle_admin(id):
    user = Admins[id]
    state = not user.active
    res = ('inactivated', 'activated')[state]
    user.active = state
    db_resp = user.save()
    print(db_resp)
    return res


def remove_admin(id):
    Admins[id].delete_instance()
