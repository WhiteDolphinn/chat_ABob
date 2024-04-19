import json

users_list = dict()


class User:
    def __init__(self, name = "username", id = 0) -> None:
        self.id        = id
        self.name      = name
        self.chats     = []

    def create_chat():
        pass

    def entry_to_chat():
        pass

    def exit_from_chat():
        pass

    def del_chat():
        pass

    def send_to():
        pass

    def ban_user():
        pass

    def to_json(self):
        return json.dumps({
            "id": self.id,
            "name": self.name,
            "chats": self.chats
        })
    
    def from_json(self, mess):
        mess = json.load(mess)
        self.id        = mess["id"]
        self.name      = mess["name"]
        self.chats     = mess["chats"]


class Chat:
    chat_id     = None
    users       = dict()
    admin       = None
    messages    = 0
