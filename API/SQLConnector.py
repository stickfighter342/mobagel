import pickle
import mysql.connector

from User import User

class SQLConnector:

    def __init__(self, h, u, p, d):
        self.db = mysql.connector.connect(host = h, user = u, password = p, database = d)
        self.db.autocommit = True
        self.cursor = self.db.cursor()


    def add_item_to_sql(self, user: User):
        name = user.username
        password = user.password
        model = pickle.dumps(user.model)
        command = 'INSERT INTO users (id, username, pass, authentication, userdata) VALUES (%s, %s, %s, %s, %s);'
        self.cursor.execute(command, (user.id, name, password, user.authentication, model))


    def update_item_to_sql(self, user: User):
        name = user.username
        password = user.password
        model = pickle.dumps(user.model)
        command = 'UPDATE users SET id = %s, username = %s, pass = %s, authentication = %s, userdata = %s WHERE id = %s;' 
        self.cursor.execute(command, (user.id, name, password, user.authentication, model, user.id))

    def get_user_from_id(self, userid):
        command = 'SELECT * FROM users WHERE id = %s'
        self.cursor.execute(command, (userid,))
        row = self.cursor.fetchone()
        if not row:
            return None
        id = row[0]
        username = row[1]
        password = row[2]
        authentication = bool(row[3])
        model = pickle.loads(row[4])
        return User(id, username, password, authentication, model)
    
    def get_user_from_username(self, username):
        command = 'SELECT * FROM users WHERE username = %s'
        self.cursor.execute(command, (username,))
        row = self.cursor.fetchone()
        if not row:
            return None
        id = row[0]
        username = row[1]
        password = row[2]
        authentication = bool(row[3])
        model = pickle.loads(row[4])
        return User(id, username, password, authentication, model)

