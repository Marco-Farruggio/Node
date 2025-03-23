class Error(Exception):
    """Base class for all custom exceptions."""
    pass

class InvalidUserIDError(Error):
    """Raised when an invalid user ID is requested."""
    def __init__(self, user_id):
        super().__init__(f"Error: User ID {user_id} does not exist.")

class UsersFileDoesNotExistError(Error):
    """Raised when the users.json file cannot be found."""
    def __init__(self):
        super().__init__(f"Error: Could not find users.json.")

class UsersFileCorruptedError(Error):
    """Raised when the users.json does not contain a valid object."""
    def __init__(self):
        super().__init__(f"Error: users.json file corrupted (no valid JSON object detected).")

class UnknownError(Error):
    """Raised when an unknown error has occured."""
    def __init__(self):
        super().__init__(f"Error: Unable to ascertain causation of error.")