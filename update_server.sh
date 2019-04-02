#!/bin/bash

cd /var/www/locker1540-server
#systemctl stop apache2
rm ini/__init__.py
rm locker_service/ini/__init__.py
git pull
cp __init__.py ini/__init__.py
cp locker_service/__init__.py locker_service/ini/__init__.py
#systemctl start apache2
echo "Server updated"
