import postgresql
import os, sys
DBIP = '89.108.103.37'
username = 'locker_admin'
password = 'locker1540_admin'
DBName = 'locker'
server_path = '/var/www/locker/server/'
dev_path = os.getcwd()
current_path = server_path
if  sys.platform == 'win32':
    current_path = dev_path
DB = postgresql.open('pq://' + username + ':' + password + '@' + DBIP + ':5432/' + DBName)


# ------------------------------------------------DATASETS------------------------------------------------ #

# -------------------------------STUDENTS------------------------------- #
students_morning = [2, 3, 4, 5, 19, 21, 24, 26]
students_day = [1, 2, 3, 5, 19, 21, 24, 26]
students_evening = [2, 3, 5, 18, 19, 21, 24, 26]
# -------------------------------TEACHERS------------------------------- #
teachers_morning = [2, 4, 5, 19, 21]
teachers_day = [1, 2, 5, 19, 21]
teachers_evening = [2, 5, 18, 19, 21]
