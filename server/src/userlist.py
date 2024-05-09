import sqlite3
import src.myjson
import src.user
from random import randint


class UsersList():
    def __init__(self) -> None:
        self.connection = sqlite3.connect("userlist.db")
        self.cursor     = self.connection.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users(
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            object TEXT NOT NULL)''')
        
        if not self.find(id=0):
            self.cursor.execute(
            "INSERT INTO Users (id, username, password, object) VALUES (?, ?, ?, ?)",
            (0, "count", f"1", 'plain text'))
            self.connection.commit()
    

    def __del__(self):
        self.connection.commit()
        self.connection.close()


    def add(self, frame = 0, username = 0, password = 0):
        if isinstance(frame, src.myjson.Sig):
            username = frame.name
            password = frame.password
        data = self.find(username = username)

        if data:
            if password == data[2]:
                user = src.user.User()
                user.from_json(data[3])
                return user
            else:
                return src.myjson.TYPE.DEN
            
        if isinstance(frame, src.myjson.Sig):
            username = frame.name
            password = frame.password

        id = self.update_amout()
        user = src.user.User(username, id)
        self.cursor.execute(
            "INSERT INTO Users (id, username, password, object) VALUES (?, ?, ?, ?)",
            (id, username, password, user.to_json()))
        self.connection.commit()
        
        return user


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
        print(self.find(username=username))
        return password == self.cursor.fetchall()[0][2]
    
    def amout(self):
        self.cursor.execute("SELECT * FROM Users WHERE username = ?", ("count",))
        return int(self.cursor.fetchall()[0][2])

    def update_amout(self):
        num = self.amout() + 1
        self.cursor.execute("UPDATE Users SET password = ? WHERE username = ?", (str(num), "count"))
        self.connection.commit()
        return num
    
    def update_user(self, user: src.user.User):
        self.cursor.execute("UPDATE Users SET object = ? WHERE username = ?", (user.to_json(), user.name))
        self.connection.commit()