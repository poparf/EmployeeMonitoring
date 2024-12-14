import os
import sqlite3
basepath = os.path.abspath(os.path.dirname(__file__))
CONNECTION_URL = basepath + '/db.sqlite3'
connection = sqlite3.connect(CONNECTION_URL)
cursor = connection.cursor()