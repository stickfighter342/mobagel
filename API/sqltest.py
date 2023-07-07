import mysql.connector
from User import User

import pickle
import base64

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="stickfighter342",
    database="users"
)

users = {}

def add_item_to_sql(cursor, user: User):
    name = user.username
    password = user.password
    model = pickle.dumps(user.model)
    users[name] = len(users)
    command = 'INSERT INTO users (id, username, pass, authentication, userdata) VALUES (%s, %s, %s, %s, %s);'
    cursor.execute(command, (users[name], name, password, user.authentication, model))


def update_item_to_sql(cursor, user: User):
    name = user.username
    password = user.password
    model = pickle.dumps(user.model)
    command = 'UPDATE users SET id = %s, username = %s, pass = %s, authentication = %s, userdata = %s WHERE id = %s;' 
    cursor.execute(command, (users[name], name, password, user.authentication, model, users[name]))

def get_info_from_sql(cursor, userid):
    command = 'SELECT * FROM users WHERE id = %d' % userid
    cursor.execute(command)
    rows = cursor.fetchall()
    

mydb.autocommit = True
cursor = mydb.cursor()


user = User(username = 'dethan', password = 'hello', authentication = True)
add_item_to_sql(cursor, user)
print(users)
user.authentication = False
update_item_to_sql(cursor, user)
get_info_from_sql(cursor, users[user.username])


