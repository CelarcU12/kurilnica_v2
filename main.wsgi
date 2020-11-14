#! /usr/bin/python3.6



import logging

import sys

logging.basicConfig(stream=sys.stderr)

sys.path.insert(0, '/home/pi/projekt/kurilnica_v2/')

from main import app as application

application.secret_key = 'secretKey'
