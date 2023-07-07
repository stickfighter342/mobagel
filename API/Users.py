from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import PyJWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from SQLConnector import SQLConnector


from User import User


class Users:
    def __init__(self, h, u, p, d):
        self.users = {}
        self.password_encrypter = CryptContext(schemes=["bcrypt"], deprecated = "auto")
        self.sql = SQLConnector(h, u, p, d)
    

    def get_user_count(self):
        return len(self.users)


    def add_user(self, username: str, password: str):
        user = self.sql.get_user_from_username(username)
        if not user:
            hashed = self.password_encrypter.hash(password)
            user = User(self.get_user_count(), username, hashed)
            self.sql.add_item_to_sql(user)
            return user
        return None

    
    def get_user_from_id(self, id: int):
        user = self.sql.get_user_from_id(id)
        return user

    def get_user_from_username(self, username: str):
        user = self.sql.get_user_from_username(username)
        return user
    
    def update_user_to_sql(self, user: User):
        self.sql.update_item_to_sql(user)
        

#####
    def set_username(self, old_username: str, new_username: str):
        
        if old_username not in self.users:
            return False
        self.users[new_username] = self.users.pop(old_username)
        self.users[new_username].set_username(new_username)
    

    def set_password(self, username: str, password: str):
        if username not in self.users:
            return False
        hashed_password = self.password_encrypter.hash(password)
        self.users[username].set_password(hashed_password)

    
    def verify_password(self, user: User, password: str):
        return self.password_encrypter.verify(password, user.password)
    
