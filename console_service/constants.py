import os
import sys

import peewee

DB = peewee.PostgresqlDatabase(None)

DB_SETTINGS = {
    'host': '',
    'database': '',
    'user': '',
    'password': '',
    'port': ''
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


# -------------------------------FLASK CONFIG---------------------------- #

templates_dir = ''
secret_key = 'secretkey'

# ------------------------------------------------DATASETS------------------------------------------------ #

# -------------------------------STUDENTS------------------------------- #
students_morning = [2, 3, 4, 5, 19, 21, 24, 26]
students_day = [1, 2, 3, 5, 19, 21, 24, 26]
students_evening = [2, 3, 5, 18, 19, 21, 24, 26]
# -------------------------------TEACHERS------------------------------- #
teachers_morning = [2, 4, 5, 19, 21]
teachers_day = [1, 2, 5, 19, 21]
teachers_evening = [2, 5, 18, 19, 21]
