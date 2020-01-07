import os
import sys

import peewee

DB = peewee.PostgresqlDatabase(None)

DB_SETTINGS = {
    'host': '89.108.103.37',
    'database': 'locker',
    'user': 'locker_admin',
    'password': 'locker1540_admin',
    'port': '5432'
}

PEEWEE_SETTINGS = {
    'autoconnect': False,
    'max_connections': 20,
    'stale_timeout': 200,
    'autorollback': True
}

server_path = '/var/www/locker/server/'
dev_path = os.getcwd()
current_path = server_path
if sys.platform == 'win32':
    current_path = dev_path

# ------------------------------------------------DATASETS------------------------------------------------ #

# -------------------------------STUDENTS------------------------------- #
students_morning = [2, 3, 4, 5, 19, 21, 24, 26]
students_day = [1, 2, 3, 5, 19, 21, 24, 26]
students_evening = [2, 3, 5, 18, 19, 21, 24, 26]
# -------------------------------TEACHERS------------------------------- #
teachers_morning = [2, 4, 5, 19, 21]
teachers_day = [1, 2, 5, 19, 21]
teachers_evening = [2, 5, 18, 19, 21]
