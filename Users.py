from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import PyJWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

from User import User

class Users:
    def __init__(self):
        self.users = {}
        self.password_encrypter = CryptContext(schemes=["bcrypt"], deprecated = "auto")
    

    def add_user(self, username: str, password: str):
        if username not in self.users:
            user = User(username, self.password_encrypter.hash(password))
            self.users[username] = user
            return user
        return None

    
    def get_user(self, username: str):
        if username not in self.users:
            return None
        return self.users[username]


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
        username = user.username
        if username not in self.users:
            return False
        return self.password_encrypter.verify(password, user.password)
    
