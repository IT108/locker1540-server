#!/bin/bash
S_SEP="'"
S_DATE=$(date)
S_PREFIX="SERVER_UPDATE_"
S_RES=$S_SEP$S_PREFIX$S_DATE$S_SEP
cd /var/www/locker/server
git add *
git commit -m "$S_RES"
git push
echo "git updated"
