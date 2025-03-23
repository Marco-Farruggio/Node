import customtkinter as ctk
import threading
import socket
import random
import struct
import json

PROGRAM_PORT = 15555
ALL_ADDRS = "0.0.0.0"
LOCAL_HOST_ADDRESS = "127.0.0.1"
ADDRESS_FAMILY = socket.AF_INET
PROTOCOL = socket.SOCK_STREAM

users = {}
users_config = {}

class ClientNode(socket.socket):
    def __init__(self, address_family, protocol, server_ip, port) -> None:
        super().__init__(address_family, protocol)

        self.SERVER_IP = server_ip
        self.PORT = port

        self.connect((self.SERVER_IP, self.PORT))

    def transmit(self, msg: str) -> None:
        self.sendall(msg.encode("utf-8"))

class ServerNode(socket.socket):
    def __init__(self, address_family, protocol, listening_addr, port) -> None:
        super().__init__(address_family, protocol)
        
        self.HOST = listening_addr
        self.PORT = port

        self.bind((self.HOST, self.PORT))

    def recvall(self, conn) -> None:
        data = conn.recv(4)
        if not data:
            return None, None

        sender_id = struct.unpack("!I", data)[0]
        message = b""

        while True:
            chunk = conn.recv(1024)

            if not chunk:
                break

            message += chunk

        return sender_id, message.decode("utf-8")

print_lock = threading.Lock()

def thread_print(txt) -> None:
    with print_lock:
        print(txt)

def server_accepting() -> None:
    server = ServerNode(ADDRESS_FAMILY, PROTOCOL, ALL_ADDRS, PROGRAM_PORT)
    server.listen()
    server_ready_event.set()

    thread_print("[ServerThread] [ServerNode] Server is listening...")

    while True:
        conn, addr = server.accept()
        thread_print(f"[ServerThread] [ServerNode] Connection accepted from {addr[0]}:{addr[1]}")

        sender_id, message = server.recvall(conn)  # Receive data (up to 1024 bytes)

        if sender_id is not None and message:
            thread_print(f"[ServerThread] [ServerNode] Received from (32BitID) {sender_id}: {message}")  # Decode and print the message

        conn.close()

class Window(ctk.CTk):
    def __init__(self, title: str, size: tuple[int, int], theme: str, accent: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        ctk.set_appearance_mode(theme)
        ctk.set_default_color_theme(accent)
        
        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}")
        self.open = True

    def run(self) -> None:
        self.mainloop()

# Base error class
class BaseError(Exception):
    """Base class for all custom exceptions."""
    pass

# Specific error for invalid user IDs
class InvalidUserIDError(BaseError):
    """Raised when an invalid user ID is requested."""
    def __init__(self, user_id):
        super().__init__(f"Error: User ID {user_id} does not exist.")

# users.json
#
# {
#     "4294967295": {
#         "username": "Username",
#         "password": "Password",
#         "ip": "127.0.0.1",
#     }
# }

def _update_users_file():
    with open("users.json", "w") as f:
        json.dump(users_config, f)

class User:
    def __init__(self, username: str, password: str, ip_address: str) -> None:
        self.__password = password
        self.id = self.generate_id()
        self.username = username
        self.ip = ip_address

        users[self.id] = self
        
        users_config[self.id] = self.get_config()
        _update_users_file()

    def generate_id(self) -> int:
        while True:
            new_id = random.randint(0, 4294967295) # 32 bit unsigned intiger
            if new_id not in users: # Check if the ID is alreayd taken (O(1))
                return new_id

    def get_config(self) -> dict:
        return {"username": self.username,
                "ip": self.ip,
                "password": self.__password}

def fetch_from_id(user_id) -> None:
    """Fetch a user object by ID"""

    result = users.get(user_id)
    if result != None:
        return result
        
    raise InvalidUserIDError(user_id)

def send_message(sender_id, target_id, message, encoding: str = "utf-8") -> None:
    """High level sending function, handles all difficulties"""

    try:
        target_ip = fetch_from_id(target_id).ip

        def send() -> None:
            client = ClientNode(ADDRESS_FAMILY, PROTOCOL, target_ip, PROGRAM_PORT)
            from_bytes = struct.pack("!I", sender_id)
            
            client.sendall(from_bytes + message.encode(encoding))
            client.close()

        thread = threading.Thread(target=send)
        thread.start()

    except InvalidUserIDError as e:
        print(f"Error in sending message: {e}")

def send_message_from_gui() -> None:
    sender_id = admin.id
    target_id = int(input_target_id.get())
    message = input_message.get()

    send_message(sender_id, target_id, message)

gui = Window("Node", (500, 500), "dark", "blue")
gui.iconbitmap("Node\icon.ico")

users_frame = ctk.CTkFrame(gui, fg_color="green", width=130, height=480)
users_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")
users_frame.pack_propagate(False)

chat_frame = ctk.CTkFrame(gui, fg_color="red", width=330, height=480)
chat_frame.grid(row=0, column=1, padx=10, pady=10, sticky="w")
chat_frame.pack_propagate(False)

server_ready_event = threading.Event()

server_thread = threading.Thread(target=server_accepting, daemon=True)

server_thread.start()
server_ready_event.wait()

input_message = ctk.CTkEntry(users_frame, placeholder_text="Message", width=100, height=20)
input_message.pack(anchor="nw")

input_target_id = ctk.CTkEntry(users_frame, placeholder_text="UserID")
input_target_id.pack(anchor="nw")

send_msg_button = ctk.CTkButton(users_frame, text="Send Message", command=send_message_from_gui, width=120, height=25)
send_msg_button.pack(anchor="n")

thread_print("[MainThread] Running GUI...")

admin = User("Admin", "Password", "127.0.0.1")
user2 = User("User2", "Password2", "127.0.0.1")

marco = User("Marc0", "Marco'sPassword", "127.0.0.1")

marco.add_friend(admin.id)
marco.add_friend(user2.id)

for friend in marco.friends:
    pass

print(f"Admin ID: {admin.id}")
print(f"User2 ID: {user2.id}")

send_message(admin.id, user2.id, "Hello User2, this is from Admin! I hope this works :D")

gui.run()