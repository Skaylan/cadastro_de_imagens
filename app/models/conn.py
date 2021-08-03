import mysql.connector


HOST = 'localhost'
USERNAME = 'root'
PASSWORD = ''
DATABASE = 'salvaimagens'

db = mysql.connector.connect(host=HOST, user=USERNAME, password=PASSWORD, database=DATABASE)
cursor = db.cursor()

