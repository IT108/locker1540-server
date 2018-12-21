import postgresql
from pyriodic import Scheduler
DBIP = '176.99.11.114'
username = 'locker'
password = 'locker1540'
DBName = 'locker'
DB = postgresql.open('pq://' + username + ':' + password + '@' + DBIP + ':5432/' + DBName)
s = Scheduler()


# ------------------------------------------------DATASETS------------------------------------------------ #

# -------------------------------STUDENTS------------------------------- #
students_morning = [2, 3, 4, 5, 19, 21, 24, 26]
students_day = [1, 2, 3, 5, 19, 21, 24, 26]
students_evening = [2, 3, 5, 18, 19, 21, 24, 26]
# -------------------------------TEACHERS------------------------------- #
teachers_morning = [2, 4, 5, 19, 21]
teachers_day = [1, 2, 5, 19, 21]
teachers_evening = [2, 5, 18, 19, 21]
