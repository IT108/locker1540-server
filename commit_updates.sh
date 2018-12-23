#!/usr/bin/expect -f
set timeout -1
spawn /bin/su root
expect "Password: "
send "ITCHURCH\r"
expect "\r\n"
send "cd /var/www/locker/server\r"
expect "root@176-99-11-114:/var/www/locker/server# "
send "git add *\r"
expect "root@176-99-11-114:/var/www/locker/server# "
send "git commit -m 'SERVER_UPDATE'\r"
expect "root@176-99-11-114:/var/www/locker/server# "
send "git push\r"
expect "root@176-99-11-114:/var/www/locker/server# "

