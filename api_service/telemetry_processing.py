import json
import sqlite3
from sqlite3 import Error
from console_service import constants
import datetime


def process_status(status):
    status = format_status(status)
    write_status(status)


def format_status(status):
    status = json.loads(status)
    return status


def write_status(status):
    conn = connect(constants.DB_NAME)
    cur = conn.cursor()
    q = 1
    for i in status:
        values = [str(q), to_sql_str(i), to_sql_str(status[i]), to_sql_str(datetime.datetime.now().isoformat(' ')[:-7])]
        sql = 'INSERT OR REPLACE INTO ' + constants.STATUS_TABLE + '(id,name,status,updated) VALUES('
        for a in values:
            sql += a + ','
        sql = sql[:-1] + ')'
        cur.execute(sql)
        q += 1
    cur.close()
    conn.commit()


def to_sql_str(a):
    return "'" + a + "'"


def select_status():
    conn = connect(constants.DB_NAME)
    cur = conn.cursor()
    cur.execute('SELECT * FROM ' + constants.STATUS_TABLE)
    r = cur.fetchall()
    res = []
    for a in r:
        p = {'id': a[0], 'name': a[1], 'status': a[2], 'updated': a[3]}
        res.append(p)
    return res


def connect(db_name):
    try:
        conn = sqlite3.connect(db_name)
        print(sqlite3.version)
        c = conn.cursor()
        c.execute(constants.create_table_command)
        c.close()
        return conn
    except Error as e:
        print(e)
