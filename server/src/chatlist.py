import sqlite3
import src.chatlist
import src.myjson
import src.user
import json
from random import randint


class ChatList():
    def __init__(self) -> None:
        self.connection = sqlite3.connect("chatlist.db")
        self.cursor     = self.connection.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Chats(
            id INTEGER PRIMARY KEY,
            admin_id INTEGER,
            object TEXT NOT NULL)''')
        
        if not self.find(id=0):
            self.cursor.execute(
            "INSERT INTO Chats (id, admin_id, object) VALUES (?, ?, ?)",
            (0, 0, f"0"))
            self.connection.commit()

    def add(self, user:src.user.User):
        chat_id = self.get_available_chat_id()
        chat = Chat(chat_id=chat_id,
                    admin_id=user.id)
        chat = chat.to_json()
        self.cursor.execute(
            "INSERT INTO Chats (id, admin_id, object) VALUES (?, ?, ?)",
            (chat_id, user.id, chat))
        self.connection.commit()
        user.chats.append(chat_id)
        return chat_id  


    def get_available_chat_id(self):
        n = int(self.find(0)[0][2]) + 1
        self.cursor.execute("UPDATE Chats SET object = ? WHERE id = ?", (str(n), 0))
        self.connection.commit()
        return n
    
    def find(self, id):
        self.cursor.execute("SELECT * FROM Chats WHERE id = ?", (id,))
        return self.cursor.fetchall()
    
    def update_chat(self, chat):
        self.cursor.execute("UPDATE Chats SET object = ? WHERE id = ?", (chat.to_json(), chat.chat_id))
        self.connection.commit()

    def delite_chat(self, chat):
        self.cursor.execute("DELETE FROM Chats WHERE id = ?", (chat.chat_id,))
        self.connection.commit()
    

class Chat():
    def __init__(self, chat_id = 0, admin_id = 0):
        self.chat_id  = chat_id
        self.admin_id = admin_id
        self.userlist = {admin_id: "admin"}

        self.connection = sqlite3.connect("database.db")
        self.cursor     = self.connection.cursor()
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS Chat{self.chat_id}(
            name TEXT NOT NULL,
            time TEXT NOT NULL,
            text TEXT NOT NULL)''')
        

    def add_user(self, user: src.user.User, added_user: src.user.User):
        if user.id == self.admin_id:
            self.userlist[added_user.id] = added_user.name
            return src.myjson.Ack()
        return src.myjson.Den()


    def del_user(self, user: src.user.User, bunned_user: src.user.User):
        if user.id == self.admin_id:
            if str(bunned_user.id) in self.userlist:
                del self.userlist[str(bunned_user.id)]
            return src.myjson.Ack()
        return src.myjson.Den()
    
    
    def ext_user(self, user: src.user.User):
        print(user.id, self.userlist)
        if str(user.id) in self.userlist:
            del self.userlist[str(user.id)]
            return src.myjson.Ack()
        return src.myjson.Den()
    

    def add_message(self, 
                    user:src.user.User, 
                    event: src.myjson.MessageFrame):
        if user.id not in self.userlist.keys():
            return src.myjson.Den()
        else:
            self.cursor.execute(
            f"INSERT INTO Chats{self.chat_id}(name, time, text) VALUES (?, ?, ?)",
            (user.name, event.time, event.text))
            return src.myjson.Ack()
    
    def to_json(self):
        return json.dumps({
            "chat_id" : self.chat_id,
            "admin_id": self.admin_id,
            "userlist": json.dumps(self.userlist)
        })
    
    def from_json(self, mess):
        if not isinstance(mess, dict):
            mess = json.loads(mess)
        self.chat_id  = mess["chat_id"]
        self.admin_id = mess["admin_id"]
        self.userlist = json.loads(mess["userlist"])
