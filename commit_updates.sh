#!/usr/bin/expect -f
S_SEP="'"
S_DATE=$(date)
S_PREFIX="SERVER_UPDATE_"
S_RES=$S_SEP$S_PREFIX$S_DATE$S_SEP
set timeout -1
spawn /bin/su root
expect "Password: "
send "ITCHURCH\r"
expect "\r\n"
send "cd /var/www/locker/server\rgit add *\rgit commit -m "$S_RES"\rgit push"