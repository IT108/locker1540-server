#!/usr/bin/expect -f
set timeout -1
spawn /var/www/locker/server/git_commit.sh
expect "Password: "
send "ITCHURCH\r"
expect "\r\n"
expect "root@176-99-11-114:/var/www/locker/server# "
expect "git updated"
