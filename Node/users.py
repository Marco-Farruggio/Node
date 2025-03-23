from typing import Union
import random
import errors
import json
import os

# users.json
#
# {
#     "4294967295": {
#         "username": "Username",
#         "password": "Password",
#         "ip": "127.0.0.1",
#     }
# }

def _purge_users(verbose: bool = True) -> None:
    validation = input("[users.py] [_purge_users] Requesting purge of all users & relevant data. Proceed (Y/N)? ").strip().lower()
    
    if validation == "y":
        with open("users.json", "w") as f:
            json.dump({}, f, indent=4)
            print("[users.py] [_purge_users] Successfully purged all users & relevant data.")
    
    elif validation == "n":
        print("[users.py] [_purge_users] Purge of all users & relevant data successfully canceled.")
    
    else:
        print("[users.py] [_purge_users] Invalid input. Purge canceled.")

def _add_user(username: str, password: str, id: Union[int, str], ip_address: str) -> None:
    # Check if file exists and read existing data
    if not os.path.exists("users.json"):
        raise errors.UsersFileDoesNotExistError()
        
    with open("users.json", "r") as f:
        try:
            old_data = json.load(f)  # Load existing JSON
        
        except json.JSONDecodeError:
            raise errors.UsersFileCorruptedError()

    # Add the new user
    old_data[str(id)] = {
        "username": username,
        "password": password,
        "ip": ip_address
    }

    # Write updated data back to file
    with open("users.json", "w") as f:
        json.dump(old_data, f, indent=4)

def user_exists(user_id: Union[int, str]) -> bool:
    # Ensure ID is a string (since JSON stores keys as strings)
    user_id = str(user_id)

    # Check if the file exists
    if not os.path.exists("users.json"):
        raise errors.UsersFileDoesNotExistError()

    # Read the file
    with open("users.json", "r") as f:
        try:
            users = json.load(f)  # Load existing users
        
        except json.JSONDecodeError:
            raise errors.UsersFileCorruptedError()

    # Check if the user ID exists in the dictionary
    return user_id in users

def search_by(criteria: str, value: Union[str, int]) -> dict:
    """
    Search for users based on a given criteria (id, username, ip)
    """

    # Ensure criteria is valid
    valid_criteria = ['id', 'username', 'ip']
    if criteria not in valid_criteria:
        raise ValueError(f"Invalid criteria. Valid options are: {', '.join(valid_criteria)}")

    # Read the users from the file
    if not os.path.exists("users.json"):
        raise FileNotFoundError("[users.py] [search_by] 'users.json' file not found.")
    
    with open("users.json", "r") as f:
        try:
            users = json.load(f)
        except json.JSONDecodeError:
            raise errors.UsersFileCorruptedError()

    # Iterate through the users and search based on the specified criteria
    for user_id, user_data in users.items():
        if criteria == 'id' and str(user_id) == str(value):  # Search by ID
            return user_data
        
        elif criteria == 'username' and user_data['username'].lower() == str(value).lower():  # Search by username
            return user_data
        
        elif criteria == 'ip' and user_data['ip'] == str(value):  # Search by IP
            return user_data

    # If no match is found
    return None

class User:
    def __init__(self, username: str, password: str, ip_address: str) -> None:
        self.__password = password
        self.id = self.generate_id()
        self.username = username
        self.ip = ip_address

        _add_user(self.username, self.__password, self.id, self.ip)

    def generate_id(self) -> int:
        while True:
            new_id = random.randint(0, 4294967295) # 32 bit unsigned intiger
            
            if not user_exists(new_id): # Check if the ID is alreayd taken (O(1))
                return new_id