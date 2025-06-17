"""
NODE
====

- This is a minimal implementation of Marco Farruggio's Node messaging app.
- Safe to use on school computers, due to no external backends.
- Legal and ethically sound.
- This program is made for educational purposes to learn about socket and internet connections.
- The creator of this program has intended it for no malictous purposes and does not hold responsibility for any.

- File size has been minimized by removing commentation and documentation, see the full version for documentation.
- All classes and even license etc has been bundled to a single file for easy distribution.
- Almost all error handling has been stripped away in the lite version, most will past under the hood without being raised.
"""

from typing import Any, Callable, Optional, Tuple, Union, List
import tkinter as tk
import threading
import socket

PADX = 10
PADY = 10
WIN_MINX = 360
WIN_MINY = 356

CONTACT_CARD_X = 100
CONTACT_CARD_Y = 150

ICON_SIZE = (16, 16)

UNLOCKED = "normal"
LOCKED = "disabled"

LOCALHOST = "127.0.0.1"
GLOBAL = "0.0.0.0"
PROGRAM_PORT = 53210
ADDRESS_FAMILY = socket.AF_INET
PROTOCOL = socket.SOCK_STREAM

DATA_CHUNK_SIZE = 1024
ENCODING = "utf-8"

LICENSE = """MIT License

Copyright (c) 2025 Marco Farruggio

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""

__version__ = "0.0.7"
__author__ = "Marco Farruggio"
__maintainer__ = "Marco Farruggio"
__email__ = "marcofarruggiopersonal@gmail.com"
__status__ = "development"
__platform__ = "Cross-platform"
__created__ = "19-05-2025"
__license__ = "MIT"
__description__ = "Stripped down Node messaging app for basic distribution"
__github__ = "https://github.com/Marco-Farruggio/Node"
__url__ = __github__


changelog = """0.0.7: Built for macOS Sonoma and reworked Settings & GUI backend handling.
0.0.6: Finished Chat displays with text.
0.0.5: Added Github Repository for cloud saving.
0.0.4: Updated settings with "Toggle Always On Top" button.
0.0.3: Refactored socket backend, added Chat specific GUI.
0.0.2: Polished GUI, added "Chat" menu, cleaned internal codes.
0.0.1: Added GUI & data transmision backend.
0.0.0: Created."""

info = f"""Node v{__version__} Lite


Author & Maintainer: Marco Farruggio

Email: marcofarruggiopersonal@gmail.com

Platform(s): Cross Platform

Created: 19/05/2025

License: MIT

Github: https://github/com/Marco-Farruggio/Node

- This is a minimal implementation of Marco Farruggio's Node messaging app.
- Safe to use on school computers, due to no external backends.
- Legal and ethically sound.
- This program is made for educational purposes to learn about socket and internet connections.
- The creator of this program has intended it for no malictous purposes and does not hold responsibility for any.

- File size has been minimized by removing commentation and documentation, see the full version for documentation.
- All classes and even license etc has been bundled to a single file for easy distribution.
- Almost all error handling has been stripped away in the lite version, most will past under the hood without being raised."""

def fetch_ip_config() -> str:
    try:
        primary_ipv4_address = socket.gethostbyname(socket.gethostname())

    except Exception as e:
        primary_ipv4_address = "Unavailable"

    try:
        hostname = socket.gethostbyname_ex(socket.gethostname())[0]
    
    except Exception as e:
        hostname = "Unavailable"

    try:
        aliases = socket.gethostbyname_ex(socket.gethostname())[1]
        aliases = ", ".join(aliases) if aliases else "None"
    
    except Exception as e:
        aliases = "Unavailable"

    try:
        associated_addresses = socket.gethostbyname_ex(socket.gethostname())[2]
        associated_addresses = ", ".join(associated_addresses)
    
    except Exception as e:
        associated_addresses = "Unavailable"

    return f"""IP Configuration:

(Socket Data):
Primary IPv4 Address: {primary_ipv4_address}

Hostname: {hostname}
Aliases: {aliases}
Associated IP Addresses: {associated_addresses}
"""

class Contact:
    def __init__(self, associated_addresses: List[str], name: str) -> None:
        self.associated_addresses = associated_addresses
        self.name = name

class ClientHandler:
    def __init__(self, func_on_add: Callable[[socket.socket, Tuple[str, int]], Optional[Any]]=None, func_on_leave: Callable[[str], Optional[Any]]=None, func_on_recieved: Callable[[str], Optional[Any]]=None) -> None:
        self.func_on_add = func_on_add
        self.func_on_leave = func_on_leave
        self.func_on_recieved = func_on_recieved

        self.server = socket.socket(ADDRESS_FAMILY, PROTOCOL)
        try:
            self.server.bind((GLOBAL, PROGRAM_PORT)) 
        
        except OSError:
            print("Unable to run concurrent instances of program at the same time. Exiting.")
            exit()
        
        self.server.listen()
        self.clients = []

        client_loop_thread = threading.Thread(target=self.client_loop, daemon=True)
        client_loop_thread.start()

    def client_loop(self):
        while True:
            client_socket, client_address = self.server.accept()
            client_thread = threading.Thread(target=self._handle_client, args=(client_socket, (client_address)), daemon=True)
            client_thread.start()

    def _handle_client(self, client_socket, client_address) -> None:
        if self.func_on_add:
            self.func_on_add(client_socket, client_address)

        self.clients.append(client_socket)

        try:
            while True:
                try:
                    data = client_socket.recv(1024)
                    
                    if data:
                        message = data.decode(ENCODING)
                            
                        if self.func_on_recieved:
                            self.func_on_recieved(f"{client_address[0]}:{client_address[1]}", message)

                    else:
                        break

                except Exception:
                    break

        finally:
            client_socket.close()
            self.clients.remove(client_socket)
            self.func_on_leave(f"{client_address[0]}:{client_address[1]}")

    def _receive_all(self, client_socket):
        data = b""

        while True:
            chunk = client_socket.recv(DATA_CHUNK_SIZE)
            
            if not chunk:
                break
            
            data += chunk
        
        return data

class ChatGUI:
    def __init__(self) -> None:
        self.client_handler = ClientHandler(self.add_client, self.remove_client, self.recieve_data)

        self.gui = tk.Tk()
        self.gui.title(f"Node Lite v{__version__}")
        self.gui.minsize(WIN_MINX, WIN_MINY)
        self.gui.geometry("540x540")

        self.viewing = "settings"
        self.topmost = False
        self.appearance_mode = "System"

        self.create_widgets()

        self.client_buttons = {}
        self.client_sockets = {}
        self.client_chats = {}
        self.current_client = None

        self.contacts = []
        self.contacts.append(Contact(["127.0.0.1"], "This PC"))
        self.contacts.append(Contact(["195.180.32.34"], "Marco Farruggio"))

    def _create_contact_card(self, contact: Contact) -> tk.Frame:
        card = tk.Frame(master=self.contacts_scrollable_frame, height=CONTACT_CARD_Y)

        def confirm_contact_name(event) -> None:
            contact.name = name_box.get("1.0", "end").strip()
            name_box.configure(state="disabled")

        edit_button = tk.Button(master=card, text="Edit", command=lambda: name_box.configure(state="normal"))
        edit_button.pack(padx=(0, 5), pady=5, side="right", anchor="n")

        name_box = tk.Text(master=card, height=contact.name.count("\n") + 1)
        name_box.insert("0.0", contact.name)
        name_box.configure(state="disabled")
        name_box.pack(pady=5, padx=5, fill="x")
        name_box.bind("<Return>", confirm_contact_name)

        addr_label = tk.Label(master=card, text=contact.associated_addresses[0]) # Primary Address
        addr_label.pack(pady=(0, 5), padx=5, fill="x")

        return card

    def create_widgets(self) -> None:
        self.menu_frame = tk.Frame(master=self.gui, width=400)
        self.menu_frame.pack(side="left", fill="y", padx=PADX, pady=PADY)

        self.display_frame = tk.Frame(master=self.gui)
        self.display_frame.pack(side="left", fill="both", expand=True, padx=PADX, pady=PADY)

        self.settings_menu_button = tk.Button(master=self.menu_frame, text="Settings", command=lambda: self.update_display("settings"))
        self.settings_menu_button.pack(pady=PADY, padx=PADX, fill="x")

        self.license_menu_button = tk.Button(master=self.menu_frame, text="License", command=lambda: self.update_display("license"))
        self.license_menu_button.pack(pady=PADY, padx=PADX, fill="x")

        self.ip_config_menu = tk.Button(master=self.menu_frame, text="Ip Config", command=lambda: self.update_display("ip_config"))
        self.ip_config_menu.pack(pady=PADY, padx=PADX, fill="x")

        self.info_menu_button = tk.Button(master=self.menu_frame, text="Info", command=lambda: self.update_display("info"))
        self.info_menu_button.pack(pady=PADY, padx=PADX, fill="x")

        self.changelog_menu_button = tk.Button(master=self.menu_frame, text="Changelog", command=lambda: self.update_display("changelog"))
        self.changelog_menu_button.pack(pady=PADY, padx=PADX, fill="x")

        self.contacts_button = tk.Button(master=self.menu_frame, text="Contacts", command=lambda: self.update_display("contacts"))
        self.contacts_button.pack(pady=PADY, padx=PADX, fill="x")

        self.new_chat_button = tk.Button(master=self.menu_frame, text="+", command=lambda: self.update_display("new_chat"))
        self.new_chat_button.pack(pady=PADY, padx=PADX, fill="x")

        self.entry_box = tk.Entry(master=self.display_frame)
        self.entry_box.bind("<Return>", lambda event: self.send_message())

        self.send_button = tk.Button(master=self.display_frame, text="Send", command=self.send_message)

        self.display_textbox = tk.Text(master=self.display_frame, wrap="word")
        self.display_textbox.configure(state="disabled")

        self.topmost_radio_button = tk.Checkbutton(self.display_frame, text="Always On Top", command=self._toggle_topmost)

        self.new_chat_ip_label = tk.Label(self.display_frame, text="New connection IP Address (IPv4): x.x.x.x")
        self.new_chat_ip_entry = tk.Entry(self.display_frame)

        self.new_chat_attempt_button = tk.Button(self.display_frame, text="Attempt Connection", command=self._new_chat)

        self.default_settings_button = tk.Button(self.display_frame, text="Reset Defaults", command=self._reset_settings)

        self.contacts_scrollable_frame = tk.Frame(master=self.display_frame)

        self.create_contact_card = tk.Frame(master=self.contacts_scrollable_frame, width=CONTACT_CARD_X, height=CONTACT_CARD_Y)

    def recieve_data(self, client_address, data: Union[str, bytes, bytearray]) -> None:
        self.client_chats[client_address] += f"Them: {data}\n"

        self.display_textbox.configure(state=UNLOCKED)
        self.display_textbox.delete("1.0", "end")
        self.display_textbox.insert("end", self.client_chats[self.current_client])
        self.display_textbox.configure(state=LOCKED)

    def _reset_settings(self) -> None:
        self.topmost_radio_button.deselect()
        self._toggle_topmost()

    def add_client(self, client_socket, client_address) -> None:
        formatted = f"{client_address[0]}:{client_address[1]}"
        self.client_sockets[formatted] = client_socket
        self.client_chats[formatted] = ""

        def on_click(addr=formatted):
            self.current_client = addr
            self.update_display("chat")

        btn = tk.Button(master=self.menu_frame, text=f"Client {formatted}", command=on_click)
        btn.pack(pady=PADX, padx=PADY, fill="x")
        self.client_buttons[formatted] = btn

    def remove_client(self, client_address):
        if isinstance(client_address, tuple):
            client_address = f"{client_address[0]}:{client_address[1]}"

        self.client_buttons[client_address].pack_forget()
        
        del self.client_buttons[client_address]
        del self.client_sockets[client_address]
        del self.client_chats[client_address]
        self.current_client = None

    def _toggle_topmost(self) -> None:
        self.gui.attributes("-topmost", not self.topmost)
        self.topmost = not self.topmost

    def _new_chat(self) -> None:
        new_chat_ip = self.new_chat_ip_entry.get()

        if not new_chat_ip:
            return
        
        try:
            client_sock = socket.socket(ADDRESS_FAMILY, PROTOCOL)
            client_sock.connect((new_chat_ip, PROGRAM_PORT))

            threading.Thread(target=self.client_handler._handle_client, args=(client_sock, (new_chat_ip, PROGRAM_PORT)), daemon=True).start()

        except Exception:
            pass

    def _hide_menu_widgets(self) -> None:
        self.default_settings_button.pack_forget()
        self.entry_box.pack_forget()
        self.send_button.pack_forget()
        self.topmost_radio_button.pack_forget()
        self.new_chat_ip_entry.pack_forget()
        self.new_chat_attempt_button.pack_forget()
        self.create_contact_card.pack_forget()
        self.display_textbox.pack_forget()
        self.contacts_scrollable_frame.pack_forget()
        self.new_chat_ip_label.pack_forget()

    def update_display(self, view: Optional[str]=None) -> None:
        if view:
            self.viewing = view

        self._hide_menu_widgets()

        if self.viewing == "settings":
            self.topmost_radio_button.pack(padx=PADX, pady=PADY)
            self.default_settings_button.pack(padx=PADX, pady=PADY)

        elif self.viewing == "license":
            self.display_textbox.pack(padx=PADX, pady=PADY, fill="both", expand=True)
            self.display_textbox.configure(state=UNLOCKED)
            self.display_textbox.delete("1.0", "end")
            self.display_textbox.insert("end", LICENSE)
            self.display_textbox.configure(state=LOCKED)

        elif self.viewing == "changelog":
            self.display_textbox.pack(padx=PADX, pady=PADY, fill="both", expand=True)

            self.display_textbox.configure(state=UNLOCKED)
            self.display_textbox.delete("1.0", "end")
            self.display_textbox.insert("end", changelog)
            self.display_textbox.configure(state=LOCKED)

        elif self.viewing == "info":
            self.display_textbox.pack(padx=PADX, pady=PADY, fill="both", expand=True)

            self.display_textbox.configure(state=UNLOCKED)
            self.display_textbox.delete("1.0", "end")
            self.display_textbox.insert("end", info)
            self.display_textbox.configure(state=LOCKED)

        elif self.viewing == "ip_config":
            self.display_textbox.pack(padx=PADX, pady=PADY, fill="both", expand=True)

            self.display_textbox.configure(state=UNLOCKED)
            self.display_textbox.delete("1.0", "end")
            self.display_textbox.insert("end", fetch_ip_config())
            self.display_textbox.configure(state=LOCKED)
        
        elif self.viewing == "chat":
            self.display_textbox.pack(padx=PADX, pady=PADY, fill="both", expand=True)

            self.display_textbox.configure(state=UNLOCKED)
            self.display_textbox.delete("1.0", "end")
            self.display_textbox.insert("end", self.client_chats[self.current_client])
            self.display_textbox.configure(state=LOCKED)

            self.entry_box.pack(pady=(0, PADY), padx=PADY, fill="x")
            self.send_button.pack(pady=(0, PADY), padx=PADY, fill="x")

        elif self.viewing == "contacts":
            self.contacts_scrollable_frame.pack(fill="both", expand=True, padx=PADX, pady=PADY)

            for child in self.contacts_scrollable_frame.winfo_children():
                child.destroy()

            for contact in self.contacts:
                self._create_contact_card(contact).pack(pady=(0, PADY), fill="x")

        elif self.viewing == "new_chat":
            self.new_chat_ip_label.pack(pady=PADY, padx=PADY, fill="x")
            self.new_chat_ip_entry.pack(pady=PADY, padx=PADY, fill="x")
            self.new_chat_attempt_button.pack(pady=(0, PADY), padx=PADY, fill="x")

    def send_message(self):
        message = self.entry_box.get().strip()

        self.entry_box.delete(0, "end")

        if not message or not self.current_client:
            return

        client_socket = self.client_sockets[self.current_client]

        try:
            client_socket.sendall(message.encode(ENCODING))

            self.client_chats[self.current_client] += f"You: {message}\n"

            self.display_textbox.configure(state=UNLOCKED)
            self.display_textbox.delete("1.0", "end")
            self.display_textbox.insert("end", self.client_chats[self.current_client])
            self.display_textbox.configure(state=LOCKED)

        except Exception as e:
            self.client_chats[self.current_client] += f"\n-----\n\nError sending: {message}\n\nError Code & Trace Back{e}\n\nIf you don't understand this, don't worry, just report it to {__author__}\n\n-----\n\n"

    def run(self) -> None:
        self.update_display()
        self.gui.mainloop()

if __name__ == "__main__":
    interface = ChatGUI()
    interface.run()