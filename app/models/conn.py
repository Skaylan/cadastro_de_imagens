import mysql.connector


HOST = 'localhost'
USERNAME = 'root'
PASSWORD = ''
DATABASE = 'salvaimagens'

db = mysql.connector.connect(host=HOST, user=USERNAME, password=PASSWORD, database=DATABASE)


# def select(query):
#     cursor = db.cursor()
#     cursor.execute(query)
#     return cursor.fetchall()

# class Database:
#     def __init__(self, host, username, password, database):
#         self.host = host
#         self.username = username
#         self.password = password
#         self.database = database

#         self.db = mysql.connector.connect(host=self.host, user=self.username, password=self.password, database=self.database)

#     def select(self, query):
#         cursor = self.db.cursor()
#         cursor.execute(query)
#         return cursor.fetchall()

#     def insert():
#         pass



# db = Database(HOST, USERNAME, PASSWORD, DATABASE)
