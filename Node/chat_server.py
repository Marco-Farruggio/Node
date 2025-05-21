"""
NODE
====
"""

# =-----=
# IMPORTS
# =-----=

import socket
import threading
from typing import Tuple
import customtkinter as ctk

# =-------=
# CTK SETUP
# =-------=

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# =-------=
# CONSTANTS
# =-------=

# CTK constants
PADX = 10          # CTK widget default padx
PADY = 10          # CTK widget default pady
CORNER_RADIUS = 10 # CTK widget default corner radius

UNLOCKED = "normal" # CTK text box unlocked state
LOCKED = "disabled" # CTK text box locked state

# IP conostants
LOCALHOST = "127.0.0.1"
GLOBAL = "0.0.0.0"
PROGRAM_PORT = 53210

DATA_CHUNK_SIZE = 1024
ENCODING = "utf-8"

# License
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

# =----------------=
# DUNDERS & METADATA
# =----------------=

__version__ = "0.0.0"
__author__ = "Marco Farruggio"
__maintainer__ = "Marco Farruggio"
__email__ = "marcofarruggiopersonal@gmail.com"
__status__ = "development"
__platform__ = "Cross-platform"
__dependencies__ = ["customtkinter"]
__created__ = "19-05-2025"
__license__ = "MIT" # Open-source community
__description__ = "Node is a lightweight, socket based, open source chat program."
__github__ = "https://github.com/Marco-Farruggio/pybernetics"
__url__ = __github__

# =-------=
# VARIABLES
# =-------=

viewing = "settings"
changelog = """"""

# =-------=
# FUNCTIONS
# =-------=

class ChatGUI:
    def __init__(self) -> None:
        # =-----=
        # CTK GUI
        # =-----=

        self.gui = ctk.CTk()
        self.gui.title("Node")
        self.gui.geometry("600x400")
        self.gui.iconbitmap("dark_mode_icon.ico")

        # =--------=
        # CTK FRAMES
        # =--------=
        
        # Menu frame (left)
        self.menu_frame = ctk.CTkFrame(master=self.gui, width=400, corner_radius=CORNER_RADIUS)
        self.menu_frame.pack(side="left", fill="y", padx=PADX, pady=PADY)

        # Display frame (right)
        self.display_frame = ctk.CTkFrame(master=self.gui, corner_radius=CORNER_RADIUS)
        self.display_frame.pack(side="left", fill="both", expand=True, padx=PADX, pady=PADY)

        # =---------=
        # CTK WIDGETS
        # =---------=

        # Menu widgets (left) (constant)
        self.settings_menu_button = ctk.CTkButton(master=self.menu_frame, text="Settings", command=lambda: self.open_view("settings"))
        self.settings_menu_button.pack(pady=PADX, padx=PADY, fill="x")

        self.license_menu_button = ctk.CTkButton(master=self.menu_frame, text="License", command=lambda: self.open_view("license"))
        self.license_menu_button.pack(pady=PADX, padx=PADY, fill="x")

        self.chat_menu_button = ctk.CTkButton(master=self.menu_frame, text="Chat", command=lambda: self.open_view("chat"))
        self.chat_menu_button.pack(pady=PADX, padx=PADY, fill="x")

        self.info_menu_button = ctk.CTkButton(master=self.menu_frame, text="Info", command=lambda: self.open_view("info"))
        self.info_menu_button.pack(pady=PADX, padx=PADY, fill="x")

        self.changelog_menu_button = ctk.CTkButton(master=self.menu_frame, text="Changelog", command=lambda: self.open_view("changelog"))
        self.changelog_menu_button.pack(pady=PADX, padx=PADY, fill="x")

        # Inside menu widgets (right) (variable)
        self.entry_box = ctk.CTkEntry(master=self.display_frame)
        self.entry_box.pack(pady=PADX, padx=PADY, fill="x")
        
        self.dark_mode_switch = ctk.CTkSwitch(self.display_frame, text="Dark Mode", command=self.toggle_theme)
        self.dark_mode_switch.toggle() # Start on (dark mode)
        
        # Display frame self.display_textbox
        self.display_textbox = ctk.CTkTextbox(master=self.display_frame)
        self.display_textbox.pack(padx=PADX, pady=PADY, fill="both", expand=True)
        self.display_textbox.configure(state="disabled")
    
    def toggle_theme(self):
        ctk.set_appearance_mode("dark" if self.dark_mode_switch.get() == 1 else "light")
        self.gui.iconbitmap("dark_mode_icon.ico" if self.dark_mode_switch.get() == 1 else "light_mode_icon.ico")

    def update_display(self):
        if viewing == "settings":
            # Hide unused widgets
            self.entry_box.pack_forget()       # Hide entry box
            self.display_textbox.pack_forget() # Hide display textbox
        
            # Show used widgets
            self.dark_mode_switch.pack(pady=PADX, padx=PADY) # Show dark mode switch

        elif viewing == "license":
            # Hide unused widgets
            self.entry_box.pack_forget()
            self.dark_mode_switch.pack_forget()

            # Show used widgets
            self.display_textbox.pack(padx=PADX, pady=PADY, fill="both", expand=True)
            self.display_textbox.configure(state=UNLOCKED)
            self.display_textbox.delete("1.0", ctk.END)
            self.display_textbox.insert(ctk.END, LICENSE)
            self.display_textbox.configure(state=LOCKED)

        elif viewing == "changelog":
            # Hide unused widgets
            self.entry_box.pack_forget() # Hide entry box

            # Show used widgets
            self.display_textbox.pack(padx=PADX, pady=PADY, fill="both", expand=True)
            
            # Configure display textbox
            self.display_textbox.configure(state=UNLOCKED)
            self.display_textbox.delete("1.0", ctk.END)
            self.display_textbox.insert(ctk.END, changelog)
            self.display_textbox.configure(state=LOCKED)

        elif viewing == "info":
            pass

        else:
            pass

    def run(self) -> None:
        self.gui.mainloop()

    def open_view(self, view: str) -> None:
        global viewing
        viewing = view
        self.update_display()

class ClientHandler:
    def __init__(self, verbose: bool = False) -> None:
        self.verbose = verbose

        # =-----------------=
        # SOCKET SERVER SETUP
        # =-----------------=

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4, TCP
        self.server.bind((GLOBAL, PROGRAM_PORT)) # Listen on 0.0.0.0 on port 53210 (PROGRAM_PORT)
        self.server.listen()
        self.clients = [] # List of active clients

        # Alert the user in the active terminal that the ClientHandler has been initiated properly, and is listening if verbose is enabled
        if verbose:
            print(f"[ClientHandler] Server listening on {GLOBAL}:{PROGRAM_PORT}")
        
        # =------------------=
        # CLIENT HANDLING LOOP
        # =------------------=

        client_loop_thread = threading.Thread(target=self.client_loop, daemon=True)
        client_loop_thread.start()

    def client_loop(self):
        while True:
            client_socket, client_address = self.server.accept() # Accept a new connection
            client_thread = threading.Thread(target=self._handle_client, args=(client_socket, client_address), daemon=True) # Create a thread to handle said client
            client_thread.start() # Start the aforementioned thread, and start loop afresh to await a new connection

    def _handle_client(self, client_socket, client_address) -> None:
        if self.verbose:
            print(f"[ClientHandlerThread: {self._format_address(client_address)}] New connection from {self._format_address(client_address)}")
        
        self.clients.append(client_socket)

        try:
            while True:
                data = self._receive_all(client_socket)

                if not data:
                    break
                
                if self.verbose:
                    print(f"[ClientHandlerThread: {self._format_address(client_address)}] Recieved Data: {data}")

        finally:
            if self.verbose:
                print(f"[ClientHandlerThread: {self._format_address(client_address)}] {self._format_address(client_address)} disconnected")
            
            self.clients.remove(client_socket)
            client_socket.close()
    
    def _format_address(self, address: Tuple[str, int]) -> str:
        return f"{address[0]}:{address[1]}"
        
    def _receive_all(self, client_socket):
        data = b""

        while True:
            chunk = client_socket.recv(DATA_CHUNK_SIZE)
            
            if not chunk:
                break  # No more data -> client is done
            
            data += chunk
        
        return data

if __name__ == "__main__":
    client_handling = ClientHandler(True)
    ui = ChatGUI()
    ui.run()
