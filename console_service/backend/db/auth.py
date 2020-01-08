import constants
from backend.db.models import *


def check_admin(admin_login, password):
    email_resp = constants.DB.execute_sql(
        "select id from public.admins where email= %s and password = crypt(%s, password)", (admin_login, password,))
    login_resp = constants.DB.execute_sql(
        "select id from public.admins where login=%s and password = crypt(%s, password)", (admin_login, password,))
    email_resp = email_resp.fetchone()
    login_resp = login_resp.fetchone()
    resp = 0
    if login_resp:
        resp = login_resp[0]
    if email_resp:
        resp = email_resp[0]
    return resp


def get_user(uid):
    try:
        resp = Admins[uid].name
    except Exception:
        return None
    return User(str(uid), [resp])