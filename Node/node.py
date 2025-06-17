"""
NODE
====

Socket based communication app developed in python and published to .exe, .dmg and .app for Windows 11 x86_64 (?<), macOS High Sierra (?+)
Developed by Marco Farruggio

Security:
---------

RSA Private & Public Key Encryption planned implementation.
SSL.
Read/Write only sockets. Code execution safe.
Built-in OS Firewall takes priority.
Optional NAT Port Forwarding for public connections.
Custom Messaging Protocol planned implementation.

Github:
-------

https://github.com/Marco-Farruggio/Node
"""

# =-----=
# IMPORTS
# =-----=

from typing import Any, Callable, Optional, Tuple, Union, List
import customtkinter as ctk
from PIL import Image
import threading
import platform
import requests
import socket
import sys
import os

# =-------=
# CTK SETUP
# =-------=

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("green")

# =-------=
# CONSTANTS
# =-------=

# CTK constants
PADX = 10          # CTK widget default padx (px)
PADY = 10          # CTK widget default pady (px)
CORNER_RADIUS = 10 # CTK widget default corner radius
WIN_MINX = 360     # CTK minimum x window size (px)
WIN_MINY = 356     # CTK minimum y window size (px)

# Contact card constants
CONTACT_CARD_X = 100
CONTACT_CARD_Y = 150

# CTK Image constants
ICON_SIZE = (16, 16)

UNLOCKED = "normal" # CTK text box unlocked state
LOCKED = "disabled" # CTK text box locked state

# IP constants
LOCALHOST = "127.0.0.1"
GLOBAL = "0.0.0.0"
PROGRAM_PORT = 53210
ADDRESS_FAMILY = socket.AF_INET # IPv4
PROTOCOL = socket.SOCK_STREAM # TCP

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

__version__ = "0.0.7"
__author__ = "Marco Farruggio"
__maintainer__ = "Marco Farruggio"
__email__ = "marcofarruggiopersonal@gmail.com"
__status__ = "development"
__platform__ = "Cross-platform" # Compiled launchers available for MacOS and Windows
__dependencies__ = ["customtkinter", "requests", "PIL"]
__created__ = "19-05-2025"
__license__ = "MIT" # Open-source community
__description__ = "Node is a lightweight, socket based, open source chat program."
__github__ = "https://github.com/Marco-Farruggio/Node"
__url__ = __github__

# =-------=
# VARIABLES
# =-------=

changelog = """NOTE:

Read changelogs bottom to top

FORMAL UPDATE LOG:

0.0.7: Built for macOS Sonoma and reworked Settings & GUI backend handling.
0.0.6: Finished Chat displays with text.
0.0.5: Added Github Repository for cloud saving.
0.0.4: Updated settings with "Toggle Always On Top" button.
0.0.3: Refactored socket backend, added Chat specific GUI.
0.0.2: Polished GUI, added "Chat" menu, cleaned internal codes.
0.0.1: Added GUI & data transmision backend.
0.0.0: Created.

INFORMAL UPDATE LOG (REALISTIC):

0.0.74: okay i added an error handling window, (im way too tired to sound happy lol)
0.0.73: first perfect build for macos high sierra, added error handling windows, planning to remove console and add internal logging. AFTER i try to make a compiler myself :sob:
0.0.72: Procrastination update, reworked settings... AGAIN OMDDSSS, now we have a dropdown menu for theme and appearance mode, reset settings now works properly, and changing appearance mode works properly now instead of breaking stuff hahaha
0.0.71: Woah edit icon (It looks trash)
0.0.7: My ear ith wingingg and it downt feewl nicey :((
0.0.69: completely reworked how i show the contacts to make it easier for me (laziness :))))
0.0.68: woah contacts time
0.0.67: RAGHGHHHHHH
0.0.66: did some research into ipv6, will incldue it later when most things support it, may add it to the ipconfig menu, idk 4now
0.0.65: added a theme selector to settings and i have to remake the widgets every time its changed lol so i put it in a function of its own :) yippe
0.0.64: Changed the GUI so now in settings the toggle topmost isnt a button lol but not a switch, idk why it was a button before, i might have been high that day idk
0.0.63: Fixed entry box locking itself :SOBOOBBB: rendered recieve messages finally, should be last update for actually send recieve basic text display, maybe bubbles later??
0.0.62: fixed a problem with displaying text lol i was forgetting to clear the text box
0.0.61: added threading asyncrhousnously for the website ip api fetching so its literally 3x faster pog
0.0.6: woah massive changes. finished off gui, added chat logs with you and them, sped up connections, finally changed to mint green aha ;) compiled to .app / exec for macOS High Sierra, finished testing!! Big droppp
0.0.597: Guess why it did the same code twice? cus i accidently wrote the same code twice RAGHGHAHGHAHSDFGAHSDFG
0.0.596: quote unquote flawlessly is also known as opens 2-3 chats for some reason :sobbbbb
0.0.595: ok i fixed a bug with starting a new chat, workes "flawlessly" ;-; now lol
0.0.594: time to change from paddleboarding-water-colour-blue to sage-green for the colour theme :OO
0.0.593: Dude ctk's text indexing is so weirddddddd but i fixed it lol
0.0.592: now store chat history in volitale memory (RAM) aka if u close the program u aint getting that back lol. made the entry box clear when u press send so it doesnt look a weird
0.0.591: fixed like 2 problems and found 3 :sob: keyerrors with clients when they leave violently :((, but dw i can handle that. Also have to remove the default Chat menu cus it shouldnt be there raghh
0.0.59: welp i finally fnished off the ip config menu, way, way too muich data im so speckle, time to work on the chat GUI
0.0.58: uhhh...   why is half of the ipconfig menu unavailable . . . :'(
0.0.57: Time to work on 0.0.6 yahoooo, im finna make the chat gui work so u can see what u both say, and make a build file for macOS (High Sierra compatable :))
0.0.56: okayy i added the () and got the function working, i would do more, but for some mysterious reason, ive decided to slepp (i wonder why . . . ;)
0.0.55: woops, i forgot (), gimme a second . . .
0.0.54: Completely revamped the ip_config page, now fetch most of the data either locally from socket, or online with apify's api, including more info, and error handling for certificates
0.0.53: me when i realise i dont even have a hashtag key so i cant rlly type comments
0.0.52: me when i accidently but an unmatched bracket on line 395 :sob: :',((
0.0.51: okayy im finally back after like a 5 day 'rest' *COUGH COUGH COUGH*, time to do some cLeAnInG
0.0.5: gonna logoff for the day so im recompiling / bundling and updating the USB, we'll see how this goes . . .
0.0.498: Made the display textbox wrap by word instead of by characters so its a lot smoother and easy to read :DD
0.0.497: cleaned up the logging on the terminal backend (u wont see this as i disabled terminal in the exe lol, but u can read it if u read the sourcecode in the USB (node.py))
0.0.496: not an update but just a note, the encoding im using is utf-8 (global standard) so emojis n' stuff will work finally
0.0.495: made a cheeky testing script which i wont add which just routes my computer to myself ;-; (its important trust)
0.0.49: THREADING UPDATES: now can reply to as many people and have as many active connections as you want at the same time (parrallel programming ohh yeahhh boii)
0.0.48: unfortunately you wont be able to see this as ive made a chat only appear if theres a connection
0.0.47: Yahhoooo the program can now: recieve messages!! AND reply !!!
0.0.465: ive been coding split screen while play a horror game with my friend xppppp what in the multitasking
0.0.46: news flash - i just added a function to remove a client, - before we can even add them . . . (uhh i may not be that smart)
0.0.465: *Queues epic banger* (okay fine why is this even on the changelog bro)
0.0.46: GREAT NEWS!!! (jk the sending doesnt work lololll)
0.0.45: woopsie e daisies i fixed the button now lol
0.0.44: ooooohhh what the gang. I accidently named ip_config_button license_config_button ages ago rahhh
0.0.43: *sigh* (Plot twist, i didnt actually sigh) Time to add some .-=tEXt=-. (haha cool shape)
0.0.42: okay dokie i fixed the fixed chat thingy on the side except theres a menu but no text :(
0.0.41: okie dokie i got the chat thingy on the side working. except theres no chat thingy on the side
0.0.4: (Procrastination Update :))) Added a lil dinky cute button which gives the window your undevided focus so now u have to look more teehee
0.0.34: okay fine there was no update im just procrastinating slepping (i do a lot of that (procrastination, not sleeping ofc)) (woah double nested brackets (very fancy))
0.0.32: First sucessfull compilation!!! (Bundled to .exe using pyinstaller) yauy (what the spelling ugh :()
0.0.3: rewrote most of the socket backend (dogwater -> feasable!!)
0.0.275: starts commenting everything up so non coders can understand my code *cough cough*
0.0.26: Wastes even more time writing the real update log xDD (waste of time very probabyl)
0.0.25: wastes an entire day making everything look good (pRoCrAsTiNaTiOn)
0.0.2: rearragned gui so its even more **SPECKAL**
0.0.1: spammed a bunch of speckle ctk widgets so it all looks nice n clean (pog)
0.0.097: AGHAHGH -oh i ran the whole program nvm it works yippee
0.0.096: Still no idea if this will work ngl lol, should prob do some more testing tbh
0.0.095: (Illegaly?) sets up port forwarding with my router woo-hoo
0.0.09: crashout cus imma run out of lil numbers for the update log soon
0.0.08: Realised that NAT forwarding is an abosulte- [REDACTED]
0.0.07: *Actively has a heart attack*
0.0.06: Actually tries to add backend
0.0.05: okay imma actually have to make the backend of this so stuff works lol (decision reached, still procrastinationg though)
0.0.0: Aww heck naw here we go"""

info = f"""Node v{__version__}


Author & Maintainer: Marco Farruggio

Email: marcofarruggiopersonal@gmail.com

Platform(s): Cross Platform

Created: 19/05/2025

License: MIT

Github: https://github/com/Marco-Farruggio/Node

Just a Dinky lil' note on Security :))

Enterprise grade security brought to you by an unpaid overworked 13 yr old boy
with the sleep schedule of a rustic looking brown worn buldovian door knob from the 1970s, undergowing refurbishment
to be used on a new office door for the CEO of a high rising tech company,
working with a mac older than you running sketchy programs that apple doesnt want
to know about, with a GPU where the only multitasking its good at is finding a way
to concurrently have a midlife crisis, existensial crisis, and end-of-life crisis,
with a tendancy to panic every 4 seconds completely disrupting all kernel threads,
also the operational speed of a potato, that is, a potato, which has no operating power,
which was the joke, in its entirety.

Actuall overview of security:

messages r secure
very secure :))
not even node can see ur messages fr
and probably not even u if i messed up somewhere
:sob:
messages pass through a TCP connection, and are encrypted with SSL,
but wait, THERES MORE, cus guess what a madlad i am and setup aysmetrical RSA
public-private key encryption, oh yeah, its me, who could have guess, marco farruggio,
(yk its too late at night when i start typing in third person ughh)
wanna know a crazy fact, the military uses 256bit RSA, I SET MINE UP WITH
40 THOUSAND BIT RSA
CAN YOU EVEN BEHIND TO FATHOM HOW BIG THAT IS
YOUR COMPUTER WOULD DIE (if i wassnt such an epic madlad coder ofc ofc)
the max value that can be stored ina 40k digit binary number is
2 ^ 40,000 -1 which is approximately equal to 10 ^ 12042
the number of atoms in the universe is estimated at 10 ^ 80
so take the number of atoms in the universe
is 10 ^ 80 or 2 ^ 265
now 2 ^ 265 is already so unconceivably large thats its not even really worth my time
explaining how proposturously large it is, that number, pales in comparison with
the encrpytion key
take the universe
double the number of atoms
double the number of atoms
and double the number of atoms
(you see where im going here)
another 39735 times
thats a lot of doubling
thats a big number
thats a MASSIVE number
ykwelse is massive?

anyways you get the idea
aint no one breaking into your texts

a note on connectinos:
tbh if u accept a connection the blame is on u man
jk jk nothing rlly bad can happen
(kinda?)
i setup port forwarding on my router so i can be connected to
RAW
so if u wanna connect to me, its port 53210 my guy
so yeah i kinda exposed myself, but i dontrlly have any vulnerabilities so its ight
(nervous chuckle)
your fine though dw
the protocols i used r binary only
no execution
(otherwise chat we may be cooked)
read/write
Yippe!
"""

def get_resource_path(filename: str) -> str:
    # Running on Windows
    if platform.system() == "Windows":
        if hasattr(sys, "_MEIPASS"):
            # Using Pyinstaller
            base_path = sys._MEIPASS
        
        else:
            # Python file ran normally
            base_path = os.path.dirname(os.path.abspath(__file__))
    
    # Running on MacOS
    elif platform.system() == "Darwin":
        if hasattr(sys, "_MEIPASS"):
            # Using Pyinstaller
            base_path = sys._MEIPASS
        
        # Using py2app bundling frozen bugs   
        elif getattr(sys, "Frozen", False):
            base_path = os.path.join(os.path.dirname(sys.executable), "..", "Resources")

        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
            
    else:
        raise_error_window("Unsupported Operating System")
    
    path = os.path.join(base_path, filename)
 
    if not os.path.exists(path):
        raise FileNotFoundError(f"Resource {filename} not found at {path}")
    
    return path

def fetch_ip_config() -> str:
    # =------------=
    # IP CONFIG INFO
    # =------------=

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

    def get_ip_info() -> None:
        response = requests.get("https://ipinfo.io/json")
        response.raise_for_status()

        global ipinfo_data
        ipinfo_data = ""
        for key, value in response.json().items():
            ipinfo_data += f"{key}: {value}\n"

    def get_ip_api_info() -> None:
        response = requests.get("http://ip-api.com/json")
        response.raise_for_status()

        global ip_api_data
        ip_api_data = ""
        for key, value in response.json().items():
            ip_api_data += f"{key}: {value}\n"

    def get_ipwhois_info() -> None:
        response = requests.get("https://ipwhois.app/json/")
        response.raise_for_status()

        global ipwhois_data
        ipwhois_data = ""
        for key, value in response.json().items():
            ipwhois_data += f"{key}: {value}\n"

    ip_info_thread = threading.Thread(target=get_ip_info, daemon=True)
    ip_api_info = threading.Thread(target=get_ip_api_info, daemon=True)
    ipwhois_info = threading.Thread(target=get_ipwhois_info, daemon=True)

    ip_info_thread.start()
    ip_api_info.start()
    ipwhois_info.start()

    ip_info_thread.join()
    ip_api_info.join()
    ipwhois_info.join()

    return f"""IP Configuration:

(Socket Data):
Primary IPv4 Address: {primary_ipv4_address}

Hostname: {hostname}
Aliases: {aliases}
Associated IP Addresses: {associated_addresses}

(ipinfo.io):
{ipinfo_data}
(ip-api.com):
{ip_api_data}
(ipwhois.app):
{ipwhois_data}
Any more information and it probably gets Illegal ;) teehee
"""

def raise_error_window(error_message: str = "An Unknown Error Occured", fatal=True) -> None:
    def _exit_with_error_code(error_code=1) -> None:
        sys.exit(error_code)

    window = ctk.CTk()
    window.title("Error Window")
    window.iconbitmap(get_resource_path("error_window_icon.ico"))
    
    message_display = ctk.CTkLabel(window, text=error_message)
    message_display.pack(padx=PADX, pady=PADY)
    exit_button = ctk.CTkButton(window, text="Terminate Process", command=_exit_with_error_code if fatal else window.destroy())
    exit_button.pack(padx=PADX, pady=PADY)
    
    window.mainloop()
    
# =-----=
# CLASSES
# =-----=

class Contact:
    def __init__(self, associated_addresses: List[str], name: str) -> None:
        self.associated_addresses = associated_addresses
        self.name = name

class ClientHandler:
    def __init__(self, verbose: bool = False, func_on_add: Callable[[socket.socket, Tuple[str, int]], Optional[Any]]=None, func_on_leave: Callable[[str], Optional[Any]]=None, func_on_recieved: Callable[[str], Optional[Any]]=None) -> None:
        self.func_on_add = func_on_add
        self.func_on_leave = func_on_leave
        self.func_on_recieved = func_on_recieved
        self.verbose = verbose
        self.log = ""

        # =-----------------=
        # SOCKET SERVER SETUP
        # =-----------------=

        self.server = socket.socket(ADDRESS_FAMILY, PROTOCOL) # IPv4, TCP
        try:
            self.server.bind((GLOBAL, PROGRAM_PORT)) # Listen on 0.0.0.0 on port 53210 (PROGRAM_PORT)
        
        except OSError:
            raise_error_window("Unable to run multiple instances concurrently.")
        
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
            client_thread = threading.Thread(target=self._handle_client, args=(client_socket, (client_address)), daemon=True) # Create a thread to handle said client
            client_thread.start() # Start the aforementioned thread, and start loop afresh to await a new connection

    def _handle_client(self, client_socket, client_address) -> None:
        log_id = f"ClientHandlerThread: {client_address[0]}:{client_address[1]}"

        if self.func_on_add:
            self.func_on_add(client_socket, client_address)

        if self.verbose:
            print(f"[{log_id}] Connected created")

        self.clients.append(client_socket)

        conn_closed_msg = "Connection closed"

        try:
            while True:
                try:
                    data = client_socket.recv(1024)
                    
                    if data:
                        message = data.decode("utf-8")
                        
                        if self.verbose:
                            print(f"[{log_id}] Recieved: {message}")
                            
                        if self.func_on_recieved:
                            self.func_on_recieved(f"{client_address[0]}:{client_address[1]}", message)

                    else:
                        conn_closed_msg = "Disconnected gracefully"

                        break
                
                except ConnectionResetError:
                    conn_closed_msg = "Disconnected forcefully"
                    
                    break
                
                except Exception as e:
                    if self.verbose:
                        print(f"[{log_id}] Error: {e}")

                    break

        finally:
            client_socket.close()
            self.clients.remove(client_socket)
            self.func_on_leave(f"{client_address[0]}:{client_address[1]}")
            
            if self.verbose:
                print(f"[{log_id}] {conn_closed_msg}")

    def _receive_all(self, client_socket):
        data = b""

        while True:
            chunk = client_socket.recv(DATA_CHUNK_SIZE)
            
            if not chunk:
                break  # No more data -> client is done
            
            data += chunk
        
        return data

class ChatGUI:
    def __init__(self) -> None:
        # =-----=
        # CTK GUI
        # =-----=

        self.client_handler = ClientHandler(True, self.add_client, self.remove_client, self.recieve_data)

        self.gui = ctk.CTk()
        self.gui.title("Node")
        self.gui.minsize(WIN_MINX, WIN_MINY)
        self.gui.geometry("540x540")
        self.gui.iconbitmap(get_resource_path("node_icon.ico"))

        # =-------=
        # VARIABLES
        # =-------=

        self.viewing = "settings"
        self.topmost = False
        self.appearance_mode = "System"

        # =-----=
        # WIDGETS
        # =-----=
        self.create_widgets()

        # =---=
        # CHATS
        # =---=
        self.client_buttons = {} # client_address -> CTkButton
        self.client_sockets = {} # client_address -> socket
        self.client_chats = {} # client_address -> chat's content
        self.current_client = None

        self.contacts = []
        self.contacts.append(Contact(["127.0.0.1"], "This PC"))
        self.contacts.append(Contact(["195.180.32.34"], "Marco Farruggio"))

    def _create_contact_card(self, contact: Contact) -> ctk.CTkFrame:
        card = ctk.CTkFrame(master=self.contacts_scrollable_frame, height=CONTACT_CARD_Y, corner_radius=CORNER_RADIUS)

        def confirm_contact_name(event) -> None:
            contact.name = name_box.get("1.0", ctk.END).strip()
            name_box.configure(state="disabled")

        edit_button = ctk.CTkButton(master=card, image=edit_icon, text="", command=lambda: name_box.configure(state="normal"), width=28)
        edit_button.pack(padx=(0, 5), pady=5, side="right", anchor="n")

        name_box = ctk.CTkTextbox(master=card, height=contact.name.count("\n") + 1)
        name_box.insert("0.0", contact.name)
        name_box.configure(state="disabled")
        name_box.pack(pady=5, padx=5, fill="x")
        name_box.bind("<Return>", confirm_contact_name)

        addr_label = ctk.CTkLabel(master=card, text=contact.associated_addresses[0]) # Primary Address
        addr_label.pack(pady=(0, 5), padx=5, fill="x")

        return card

    def create_widgets(self) -> None:
        # =--------=
        # CTK FRAMES
        # =--------=

        # Menu frame (left)
        self.menu_frame = ctk.CTkFrame(master=self.gui, width=400, corner_radius=CORNER_RADIUS)
        self.menu_frame.pack(side="left", fill="y", padx=PADX, pady=PADY)

        # Display frame (right)
        self.display_frame = ctk.CTkFrame(master=self.gui, corner_radius=CORNER_RADIUS)
        self.display_frame.pack(side="left", fill="both", expand=True, padx=PADX, pady=PADY)

        # =--------------=
        # CTK MENU WIDGETS
        # =--------------=

        # Menu widgets (left) (constant)
        self.settings_menu_button = ctk.CTkButton(master=self.menu_frame, text="Settings", command=lambda: self.update_display("settings"))
        self.settings_menu_button.pack(pady=PADY, padx=PADX, fill="x")

        self.license_menu_button = ctk.CTkButton(master=self.menu_frame, text="License", command=lambda: self.update_display("license"))
        self.license_menu_button.pack(pady=PADY, padx=PADX, fill="x")

        self.ip_config_menu = ctk.CTkButton(master=self.menu_frame, text="Ip Config", command=lambda: self.update_display("ip_config"))
        self.ip_config_menu.pack(pady=PADY, padx=PADX, fill="x")

        self.info_menu_button = ctk.CTkButton(master=self.menu_frame, text="Info", command=lambda: self.update_display("info"))
        self.info_menu_button.pack(pady=PADY, padx=PADX, fill="x")

        self.changelog_menu_button = ctk.CTkButton(master=self.menu_frame, text="Changelog", command=lambda: self.update_display("changelog"))
        self.changelog_menu_button.pack(pady=PADY, padx=PADX, fill="x")

        self.contacts_button = ctk.CTkButton(master=self.menu_frame, text="Contacts", command=lambda: self.update_display("contacts"))
        self.contacts_button.pack(pady=PADY, padx=PADX, fill="x")

        self.new_chat_button = ctk.CTkButton(master=self.menu_frame, text="+", command=lambda: self.update_display("new_chat"))
        self.new_chat_button.pack(pady=PADY, padx=PADX, fill="x")

        # =-----------------=
        # CTK IN MENU WIDGETS
        # =-----------------=

        # Text input box
        self.entry_box = ctk.CTkEntry(master=self.display_frame)
        self.entry_box.bind("<Return>", lambda event: self.send_message())

        self.send_button = ctk.CTkButton(master=self.display_frame, text="Send", command=self.send_message)

        # Appearance Mode widgets
        self.set_appearance_mode_label = ctk.CTkLabel(self.display_frame, text="Appearance Mode")
        self.set_appearance_mode_option_menu = ctk.CTkOptionMenu(self.display_frame, values=["System", "Light", "Dark"], command=self._set_appearance_mode)

        # Display frame self.display_textbox
        self.display_textbox = ctk.CTkTextbox(master=self.display_frame, wrap="word")
        self.display_textbox.configure(state="disabled")

        # Toggle always on top button
        self.topmost_switch = ctk.CTkSwitch(self.display_frame, text="Always On Top", command=self._toggle_topmost)

        self.new_chat_ip_entry = ctk.CTkEntry(self.display_frame, placeholder_text="x.x.x.x")
        self.new_chat_ip_entry.bind("<Return>", self._new_chat)

        self.new_chat_attempt_button = ctk.CTkButton(self.display_frame, text="Attempt Connection", command=self._new_chat)

        self.default_settings_button = ctk.CTkButton(self.display_frame, text="Reset Defaults", command=self._reset_settings)

        self.set_theme_label = ctk.CTkLabel(self.display_frame, text="Set Theme")
        self.set_theme_dropdown = ctk.CTkOptionMenu(self.display_frame, values=["Green", "Blue", "Dark Blue"], command=self._set_theme)
        
        self.contacts_scrollable_frame = ctk.CTkScrollableFrame(master=self.display_frame, corner_radius=CORNER_RADIUS)

        self.create_contact_card = ctk.CTkFrame(master=self.contacts_scrollable_frame, width=CONTACT_CARD_X, height=CONTACT_CARD_Y, corner_radius=CORNER_RADIUS)

    def _set_appearance_mode(self, choice: str) -> None:
        """Set the GUI appearance mode based on the selection."""
        ctk.set_appearance_mode(choice.lower())
        self.appearance_mode = choice
    
    def _set_theme(self, theme: str) -> None:
        # Kill all the children
        for child in self.gui.winfo_children():
            child.destroy()

        ctk.set_default_color_theme("dark-blue" if theme == "Dark Blue" else theme.lower())  # options: "blue", "dark-blue", "green"
        self.create_widgets()
        self.set_theme_dropdown.set(theme)
        self.set_appearance_mode_option_menu.set(self.appearance_mode)
        
        if self.topmost:
            self.topmost_switch.select()
            
        for addr in self.client_buttons:
            def on_click(addr=addr):
                self.current_client = addr
                self.update_display("chat")

            btn = ctk.CTkButton(master=self.menu_frame, text=f"Client {addr}", command=on_click)
            btn.pack(pady=PADX, padx=PADY, fill="x")
            self.client_buttons[addr] = btn

        self.update_display()

    def recieve_data(self, client_address, data: Union[str, bytes, bytearray]) -> None:
        self.client_chats[client_address] += f"Them: {data}\n"

        # Configure display to display the recieved message
        self.display_textbox.configure(state=UNLOCKED)
        self.display_textbox.delete("1.0", ctk.END)
        self.display_textbox.insert(ctk.END, self.client_chats[self.current_client])
        self.display_textbox.configure(state=LOCKED)

    def _reset_settings(self) -> None:
        self.set_appearance_mode_option_menu.set("Dark")
        self._set_appearance_mode("Dark")

        self.set_theme_dropdown.set("Green")
        self._set_theme("Green")
        
        if self.topmost_switch.get() != 0:
            self.topmost_switch.toggle()

    def add_client(self, client_socket, client_address) -> None:
        formatted = f"{client_address[0]}:{client_address[1]}"
        self.client_sockets[formatted] = client_socket
        self.client_chats[formatted] = ""

        def on_click(addr=formatted):
            self.current_client = addr
            self.update_display("chat")

        btn = ctk.CTkButton(master=self.menu_frame, text=f"Client {formatted}", command=on_click)
        btn.pack(pady=PADX, padx=PADY, fill="x")
        self.client_buttons[formatted] = btn

    def remove_client(self, client_address):
        self.client_buttons[client_address].pack_forget() # Hide button

        del self.client_buttons[client_address] # Delete button from list of client chat buttons (dict)
        del self.client_sockets[client_address] # Remove client's socket object from the list of sockets (dict)
        del self.client_chats[client_address] # Delete chat data (May be removed later, with saving to .txt/.csv/.bin
        self.current_client = None

    def _toggle_topmost(self) -> None:
        """
        Toggles the topmost attribute of the main ctk window ("-topmost")
        """

        self.gui.attributes("-topmost", bool(self.topmost_switch.get()))
        self.topmost = bool(self.topmost_switch.get())

    def _toggle_theme(self) -> None:
        """
        Toggles the CTK appearance theme
        """

        ctk.set_appearance_mode("dark" if self.dark_mode_switch.get() == 1 else "light")

    def _new_chat(self) -> None:
        # Setup socket
        new_chat_ip = self.new_chat_ip_entry.get().strip()

        if not new_chat_ip:
            return
        
        try:
            client_sock = socket.socket(ADDRESS_FAMILY, PROTOCOL)
            client_sock.connect((new_chat_ip, PROGRAM_PORT))

            threading.Thread(target=self.client_handler._handle_client, args=(client_sock, (new_chat_ip, PROGRAM_PORT)), daemon=True).start()

        except ConnectionRefusedError:
            print("Connection refused")

        except Exception as e:
            print(f"Error: {e}")

    def _hide_menu_widgets(self) -> None:
        # =-----------------=
        # HIDE UNUSED WIDGETS
        # =-----------------=
        self.default_settings_button.pack_forget()
        self.entry_box.pack_forget()
        self.set_appearance_mode_label.pack_forget()
        self.set_appearance_mode_option_menu.pack_forget()
        self.send_button.pack_forget()
        self.topmost_switch.pack_forget()
        self.new_chat_ip_entry.pack_forget()
        self.new_chat_attempt_button.pack_forget()
        self.set_theme_dropdown.pack_forget()
        self.create_contact_card.pack_forget()
        self.display_textbox.pack_forget()
        self.contacts_scrollable_frame.pack_forget()
        self.set_theme_label.pack_forget()

    def update_display(self, view: Optional[str]=None) -> None:
        if view:
            self.viewing = view

        self._hide_menu_widgets()

        if self.viewing == "settings":
            # =---------------=
            # SHOW USED WIDGETS
            # =---------------=
            
            # Show appearance mode selection widgets
            self.set_appearance_mode_label.pack(padx=PADX, pady=(PADY, 0))
            self.set_appearance_mode_option_menu.pack(padx=PADX, pady=PADY)
            
            # Show theme selector drop down
            self.set_theme_label.pack(padx=PADX, pady=0)
            self.set_theme_dropdown.pack(padx=PADX, pady=PADY)
            
            # Show toggle topmost switch
            self.topmost_switch.pack(padx=PADX, pady=PADY)
            
            # Show reset to default settings button
            self.default_settings_button.pack(padx=PADX, pady=PADY) # Show the reset settings button
        
        elif self.viewing == "license":
            # Show used widgets
            self.display_textbox.pack(padx=PADX, pady=PADY, fill="both", expand=True)
            self.display_textbox.configure(state=UNLOCKED)
            self.display_textbox.delete("1.0", ctk.END)
            self.display_textbox.insert(ctk.END, LICENSE)
            self.display_textbox.configure(state=LOCKED)

        elif self.viewing == "changelog":
            # Show used widgets
            self.display_textbox.pack(padx=PADX, pady=PADY, fill="both", expand=True)
            
            # Configure display textbox
            self.display_textbox.configure(state=UNLOCKED)
            self.display_textbox.delete("1.0", ctk.END)
            self.display_textbox.insert(ctk.END, changelog)
            self.display_textbox.configure(state=LOCKED)

        elif self.viewing == "info":
            # Show used widgets
            self.display_textbox.pack(padx=PADX, pady=PADY, fill="both", expand=True)

            # Configure display textbox
            self.display_textbox.configure(state=UNLOCKED)
            self.display_textbox.delete("1.0", ctk.END)
            self.display_textbox.insert(ctk.END, info)
            self.display_textbox.configure(state=LOCKED)

        elif self.viewing == "ip_config":
            # Show used widgets
            self.display_textbox.pack(padx=PADX, pady=PADY, fill="both", expand=True)

            # Configure display textbox
            self.display_textbox.configure(state=UNLOCKED)
            self.display_textbox.delete("1.0", ctk.END)
            self.display_textbox.insert(ctk.END, fetch_ip_config()) # Load entire config every time it's open, improve in 0.0.7
            self.display_textbox.configure(state=LOCKED)
        
        elif self.viewing == "chat":
            # Show used widgets
            self.display_textbox.pack(padx=PADX, pady=PADY, fill="both", expand=True)

            # Configure display textbox
            self.display_textbox.configure(state=UNLOCKED)
            self.display_textbox.delete("1.0", ctk.END)
            self.display_textbox.insert(ctk.END, self.client_chats[self.current_client])
            self.display_textbox.configure(state=LOCKED)

            self.entry_box.pack(pady=(0, PADY), padx=PADY, fill="x")
            self.send_button.pack(pady=(0, PADY), padx=PADY, fill="x")

        elif self.viewing == "contacts":
            # =---------------=
            # SHOW USED WIDGETS
            # =---------------=
            self.contacts_scrollable_frame.pack(fill="both", expand=True, padx=PADX, pady=PADY)
            
            global edit_icon
            edit_icon = ctk.CTkImage(Image.open(get_resource_path("edit_icon.png")), size=ICON_SIZE)

            for child in self.contacts_scrollable_frame.winfo_children():
                child.destroy()

            for contact in self.contacts:
                self._create_contact_card(contact).pack(pady=(0, PADY), fill="x")

        elif self.viewing == "new_chat":
            # Show required widgets
            self.new_chat_ip_entry.pack(pady=PADY, padx=PADY, fill="x")
            self.new_chat_attempt_button.pack(pady=(0, PADY), padx=PADY, fill="x")

    def send_message(self):
        message = self.entry_box.get().strip()

        # Clear message box
        self.entry_box.delete(0, ctk.END)

        if not message or not self.current_client:
            return

        client_socket = self.client_sockets[self.current_client]

        try:
            client_socket.sendall(message.encode(ENCODING))

            # Update the chat history
            self.client_chats[self.current_client] += f"You: {message}\n"

            # Configure display to add new message
            self.display_textbox.configure(state=UNLOCKED)
            self.display_textbox.delete("1.0", ctk.END)
            self.display_textbox.insert(ctk.END, self.client_chats[self.current_client])
            self.display_textbox.configure(state=LOCKED)

        except Exception as e:
            print(f"Error sending to {self.current_client}: {e}")
            self.client_chats[self.current_client] += f"\n-----\n\nError sending: {message}\n\nError Code & Trace Back{e}\n\nIf you don't understand this, don't worry, just report it to {__author__}\n\n-----\n\n"

    def run(self) -> None:
        """
        Starts GUI mainloop via CTK backend
        Initializes in Settings
        """
        # =-----=
        # RUN GUI
        # =-----=

        self.update_display() # Ensure right widgets are initially rendered
        self.gui.mainloop() # Run the gui window

if __name__ == "__main__":
    interface = ChatGUI()
    interface.run()