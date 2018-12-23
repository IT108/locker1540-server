#!/usr/local/bin/expect --

spawn su it108_admin
expect "Password: "
send "ITCHURCH\r"
spawn sudo -s
expect "[sudo] password for it108_admin: "
send "ITCHURCH\r"
sh /var/www/locker/server/git_commit.sh