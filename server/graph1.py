import tkinter as tk
from tkinter import ttk, messagebox
from src.myjson import *
import interface

class MessengerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Messenger")
        self.inter = interface.Interface()
        self.chat_id = 1
        self.last_message_id = 0

        self.current_user = None  # Store current user info
        self.chats = []  # List to store chat names or IDs

        style = ttk.Style()
        style.theme_use('clam')
        root.configure(bg="#aaaaaa")
        style.configure("TFrame", background="#5c5c5c")
        style.configure("TLabel", background="#5c5c5c", foreground="#d4d4d4", font=("Helvetica", 12))
        style.configure("TEntry", fieldbackground="#3c3c3c", background="#5c5c5c", foreground="#d4d4d4", font=("Helvetica", 12))
        style.configure("TButton", background="#3c3c3c", foreground="#ffffff", font=("Helvetica", 12, "bold"))
        style.configure("TCombobox", fieldbackground="#3c3c3c", background="#5c5c5c", foreground="#d4d4d4", font=("Helvetica", 12))

        self.user_frame = ttk.LabelFrame(root, text="Register User")
        
        self.user_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(self.user_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = ttk.Entry(self.user_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.user_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = ttk.Entry(self.user_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(self.user_frame, text="Register", command=self.register_user).grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Display current user info
        self.current_user_frame = ttk.LabelFrame(root, text="Current User Info")
        self.current_user_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.current_user_label = ttk.Label(self.current_user_frame, text="No user registered.")
        self.current_user_label.grid(row=0, column=0, padx=5, pady=5)

        # Chat management frame
        self.chat_frame = ttk.LabelFrame(root, text="Chat Management")
        self.chat_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        ttk.Button(self.chat_frame, text="Create Chat", command=self.create_chat).grid(row=0, column=0, padx=5, pady=5)
        
        ttk.Label(self.chat_frame, text="User ID:").grid(row=1, column=0, padx=5, pady=5)
        self.user_id_entry = ttk.Entry(self.chat_frame)
        self.user_id_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.chat_frame, text="Chat ID:").grid(row=2, column=0, padx=5, pady=5)
        self.chat_id_entry = ttk.Entry(self.chat_frame)
        self.chat_id_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Button(self.chat_frame, text="Add User to Chat", command=self.add_user_to_chat).grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        ttk.Label(self.chat_frame, text="Select Chat:").grid(row=4, column=0, padx=5, pady=5)
        self.chat_combobox = ttk.Combobox(self.chat_frame, values=self.chats)
        self.chat_combobox.grid(row=4, column=1, padx=5, pady=5)
        self.chat_combobox.bind("<<ComboboxSelected>>", self.chat_selected)

        # Messaging frame
        self.message_frame = ttk.LabelFrame(root, text="Messaging")
        self.message_frame.grid(row=0, column=1, rowspan=4, padx=10, pady=10, sticky="nsew")

        self.message_listbox = tk.Listbox(self.message_frame, bg="#1e1e1e", fg="#d4d4d4", selectbackground="#007acc", font=("Helvetica", 12))
        self.message_listbox.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        self.message_entry = ttk.Entry(self.message_frame)
        self.message_entry.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        ttk.Button(self.message_frame, text="Send", command=self.send_message).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(self.message_frame, text="Update", command=self.update_chat).grid(row=3, column=1, columnspan=2, padx=5, pady=5)

        # Exit button
        self.exit_button = ttk.Button(root, text="Exit", command=self.exit_app)
        self.exit_button.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

        # Configure grid to expand
        root.columnconfigure(1, weight=1)
        root.rowconfigure(3, weight=1)
        self.message_frame.rowconfigure(0, weight=1)
        self.message_frame.columnconfigure(0, weight=1)

    def register_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        print(username, password)
        sig = Sig(name=username, password=password)
        frame = self.inter.send_and_get(sig)
        print(frame)
        if frame.type == TYPE.INF:
            self.chats = frame.user.chats
            self.update_chat_combobox()
            self.current_user = {"username": username, "id": frame.user.id}  # Example ID
            self.current_user_label.config(text=f"Username: {username}\nID: {frame.user.id}")
            messagebox.showinfo("Register", f"User {username} registered!")
        else:
            messagebox.showerror("Register", "Username and Password cannot be empty.")
    
    def create_chat(self):
        frame = ControlFrame(action=ACTION.CREAT)
        frame = self.inter.send_and_get(frame)
        
        if frame.type == TYPE.ACK:
            chat_id = frame.mess.get("chat_id")  # Assuming chat_id is returned in the ACK frame
            self.chats.append(f"Chat {chat_id}")
            self.update_chat_combobox()
            messagebox.showinfo("Chat", f"Chat {chat_id} registered!")
            new_chat_window = tk.Toplevel(self.root)
            new_chat_window.title("New Chat")
            new_chat_window.protocol("WM_DELETE_WINDOW", new_chat_window.destroy)
            ttk.Label(new_chat_window, text="New chat created!").pack(padx=10, pady=10)
            ttk.Button(new_chat_window, text="Close", command=new_chat_window.destroy).pack(padx=10, pady=10)
        else:
            messagebox.showinfo("Chat", "Error creating chat.")

    def add_user_to_chat(self):
        user_id = self.user_id_entry.get()
        chat_id = self.chat_id_entry.get()
        frame = ControlFrame(action=ACTION.ADD, user_id=int(user_id), chat_id=int(chat_id))
        frame = self.inter.send_and_get(frame)
        if frame.type == TYPE.ACK:
            messagebox.showinfo("Add User", f"User {user_id} added to Chat {chat_id}!")
            self.chats.append(f"Chat {chat_id}")  # Add the chat to the list
            self.update_chat_combobox()
        else:
            messagebox.showerror("Add User", "User ID and Chat ID cannot be empty.")
    
    def chat_selected(self, s):
        self.chat_id = int(self.chat_combobox.get())
        self.message_listbox.delete(0, tk.END)
        selected_chat = self.chat_combobox.get()
        for i in range(1,1000):
            frame = PullFrame(chat_id=self.chat_id, message_id=i)
            frame = self.inter.send_and_get(frame)
            if frame.type == TYPE.CHT:
                self.message_listbox.insert(tk.END, f"{frame.message[0][2]}: {frame.message[0][4]}")
            else:
                self.last_message_id = i
                break
        

    def send_message(self):
        message = self.message_entry.get()
        frame = MessageFrame(chat_id=self.chat_id, text=message)
        frame = self.inter.send_and_get(frame)
        if frame.type == TYPE.ACK:
            self.message_entry.delete(0, tk.END)
            for i in range(self.last_message_id,100000):
                frame = PullFrame(chat_id=self.chat_id, message_id=i)
                frame = self.inter.send_and_get(frame)
                if frame.type == TYPE.CHT:
                    self.message_listbox.insert(tk.END, f"{frame.message[0][2]}: {frame.message[0][4]}")
                else:
                    self.last_message_id = i
                    break
        else:
            messagebox.showerror("Send Message", "Message cannot be empty.")
    
    def update_chat(self):
        self.message_listbox.delete(0, tk.END)
        for i in range(1,100000):
                frame = PullFrame(chat_id=self.chat_id, message_id=i)
                frame = self.inter.send_and_get(frame)
                if frame.type == TYPE.CHT:
                    self.message_listbox.insert(tk.END, f"{frame.message[0][2]}: {frame.message[0][4]}")
                else:
                    self.last_message_id = i
                    break




    def update_chat_combobox(self):
        self.chat_combobox['values'] = self.chats

    def exit_app(self):
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = MessengerApp(root)
    root.mainloop()
