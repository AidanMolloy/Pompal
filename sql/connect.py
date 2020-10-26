#!/usr/local/bin/python3

import pymysql as db
from cgitb import enable
enable()

from cgi import FieldStorage
from html import escape


connection = db.connect('***', '***', '***', '***')
cursor = connection.cursor(db.cursors.DictCursor)