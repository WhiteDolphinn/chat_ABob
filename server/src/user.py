import json

users_list = dict()


class User:
    def __init__(self, name = "username", id = 0, stream_id = 0) -> None:
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
        self.id        = js_mess[0]
        self.name      = js_mess[1]
        self.chats     = js_mess[2]


class Chat:
    chat_id     = None
    admin       = None
    users       = []
    messages    = 0
