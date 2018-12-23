#!/usr/bin/expect -f
set timeout -1
spawn /bin/su root
expect "Password: "
send "ITCHURCH\r"
expect "\r\n"
send "sh /var/www/locker/server/git_commit.sh"
