import user
import _gui

chat_ids = {}
user_ids = {}

def push_message(current_chat, message):
    user.a.send_message(message, chat_ids[current_chat])
    print(f"python:{message}")

def create_chat(chat_and_user_names):
    start = chat_and_user_names.index(":")
    chat_name = chat_and_user_names[:start]
    users_name = []
    i = chat_and_user_names.find(start, ",")
    while i != -1:
        users_name.append(chat_and_user_names[start + 1:i])
        start = i
        i = chat_and_user_names.find(start, ",")
    users_name.append(chat_and_user_names[start + 1:])
