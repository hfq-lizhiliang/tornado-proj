# coding: utf-8


import MySQLdb

conn = MySQLdb.connect(host="localhost", user="root", passwd="", db="test", port=3306, charset="utf-8")
cur = conn.cursor()