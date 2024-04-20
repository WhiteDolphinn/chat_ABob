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
    
    def from_json(self, js_mess):
        js_mess = json.loads(js_mess)
        print(js_mess)
        self.id        = js_mess['id']
        self.name      = js_mess["name"]
        self.chats     = js_mess['chats']


class Chat:
    users       = []
    messages    = []

    def __init__(self, id, admin):
        self.chat_id = id
        self.admin = admin

    




