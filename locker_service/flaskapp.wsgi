#!/usr/bin/python3
import sys
import logging
import postgresql
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/locker/server/locker_service")
from ini import app as application
