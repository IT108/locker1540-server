#!/usr/bin/expect -f

spawn ./git_commit.sh
expect "Password: "
send -- "ITCHURCH\r"
expect "[sudo] password for it108_admin: "
send -- "ITCHURCH\r"
expect eof
