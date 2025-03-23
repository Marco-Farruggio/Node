"""
Node
====

Lightweight messaging app using socket based ip - ip communication in python
"""

from typing import Union
import threading
import requests
import socket
import json
import os

import packer
import errors
import client
import server
import users
import gui

__version__ = "0.0.1"
__author__ = "Marco Farruggio"
__maintainer__ = "Marco Farruggio"
__email__ = "marcofarruggiopersonal@gmail.com"
__status__ = "development"
__platform__ = "Cross-platform"
__dependencies__ = ["customtkinter"]
__created__ = "2025-2-0"
__license__ = "MIT"
__description__ = "Node is a lightweight socket based messaging app"

PROGRAM_PORT = 15555
ALL_ADDRS = "0.0.0.0"
LOCAL_HOST_ADDRESS = "127.0.0.1"
ADDRESS_FAMILY = socket.AF_INET
PROTOCOL = socket.SOCK_STREAM
ENCODING = "utf-8"

def init_json() -> None:
    if not os.path.exists("users.json"):
        with open("users.json", "w") as f:
            json.dump({}, f, indent=4)
        
        print("[main.py] [init_json] 'users.json' file created successfully.")

def _get_public_ipv4() -> str:
    try:
        response = requests.get("https://api.ipify.org", timeout=5)
        response.raise_for_status()  # Raise an error for bad responses
        return response.text
    
    except requests.RequestException as e:
        return f"Error fetching public IPv4: {e}"

def ts_print(txt: str) -> None:
    with print_lock:
        print(txt)

def server_accepting() -> None:
    server_listening.set()
    srvr = server.ServerNode(ADDRESS_FAMILY, PROTOCOL, ALL_ADDRS, PROGRAM_PORT)
    srvr.listen()
    ts_print("[ServerThread] [ServerNode] Server is listening...")
    server_listening.set()
    
    while True:
        conn, addr = srvr.accept()
        ts_print(f"[ServerThread] [ServerNode] Connection accepted from {addr[0]}:{addr[1]}")

        sender_id, message = srvr.recvall(conn)  # Receive data (up to 1024 bytes)

        if sender_id is not None and message:
            ts_print(f"[ServerThread] [ServerNode] Received from (32BitID) {sender_id}: {message}")  # Decode and print the message

        conn.close()

def send_message(sender_id: Union[int, str], target_id: Union[int, str], message: str, encoding: str) -> None:
    """High level sending function, handles all difficulties"""

    try:
        target_ip = users.search_by("id", target_id)["ip"]

        def _send() -> None:
            clnt = client.ClientNode(ADDRESS_FAMILY, PROTOCOL, target_ip, PROGRAM_PORT)
            clnt.sendall(packer.pack(sender_id, message, encoding))
            clnt.close()

        thread = threading.Thread(target=_send)
        thread.start()

    except errors.InvalidUserIDError as e:
        print(f"Error in sending message: {e}")

public_ip = _get_public_ipv4()
init_json()

print_lock = threading.Lock()
server_listening = threading.Event()

window = gui.Window("Node", (500, 500), "dark", "blue", "Node\icon.ico")

server_thread = threading.Thread(target=server_accepting, daemon=True)

current_user = users.User("User1", "User1Password", "127.0.0.1")
user2 = users.User("User2", "User2Password", "127.0.0.1")

ts_print(f"[MainThread] Public IPv4 Address: {public_ip}")

server_thread.start()
server_listening.wait()

send_message(current_user.id, user2.id, "Hello User2, this is from User1", ENCODING)
send_message(user2.id, current_user.id, "Hello User1, this is from User2", ENCODING)

ts_print("[MainThread] Running GUI...")
window.run()