#!/usr/bin/env python3
import datetime
import postgresql
import csv
DBIP = '176.99.11.114'
username = 'locker_admin'
password = 'locker1540_admin'
DBName = 'locker'
DB = postgresql.open('pq://' + username + ':' + password + '@' + DBIP + ':5432/' + DBName)
time = datetime.datetime.now()
filename = "/var/www/locker/server/logs/" + str(time.day) + '.' + str(time.month) + '.' + str(time.year) + '.log.csv'
i = []
q = DB.query('select id, name, today_login from public.users order by id')
for a in q:
    i.append([a[0], a[1], a[2]])
with open(filename, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(i)
DB.query('update public.users set today_login=0')
