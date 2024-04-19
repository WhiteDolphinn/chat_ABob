import sqlite3
import src.myjson
from random import randint


class UsersList():
    def __init__(self) -> None:
        self.connection = sqlite3.connect("database.db")
        self.cursor     = self.connection.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users(
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL)''')
        
        if not self.find(id=0):
            self.cursor.execute(
            "INSERT INTO Users (id, username, password) VALUES (?, ?, ?)",
            (0, "count", f"1"))
    

    def __del__(self):
        self.connection.commit()
        self.connection.close()


    def add(self, frame = 0, name = 0, password = 0):
        if self.find(frame, name): 
            if self.auth(frame = 0, name = 0, password = 0):
                return src.myjson.TYPE.ACK
            else:
                return src.myjson.TYPE.DEN
            
        if isinstance(frame, src.myjson.Sig):
            username = frame.name
            password = frame.password

        id = self.amout()+1
        self.update_amout()
        self.cursor.execute(
            "INSERT INTO Users (id, username, password) VALUES (?, ?, ?)",
            (id, username, password))
        pass


    def rm(self, frame = 0, name = 0):
        pass


    def find(self, frame = 0, username = 0, id = -1):
        if id != -1:
            self.cursor.execute("SELECT * FROM Users WHERE id = ?", (id,))
            return  self.cursor.fetchone()
        
        if isinstance(frame, src.myjson.Sig):
            username = frame.name

        self.cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
        return  self.cursor.fetchone()
    

    def auth(self, frame = 0, username = 0, password = 0):
        if isinstance(frame, src.myjson.Sig):
            username = frame.name
            password = frame.password
        self.cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
        return password == self.cursor.fetchone()[0][2]
    
    def amout(self):
        self.cursor.execute("SELECT * FROM Users WHERE username = ?", ("count",))
        return int(self.cursor.fetchall()[0][2])

    def update_amout(self):
        num = self.amout()
        self.cursor.execute("UPDATE Users SET password = ? WHERE username = ?", (str(num), "count"))