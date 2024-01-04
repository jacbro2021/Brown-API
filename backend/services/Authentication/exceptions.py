"""This file contains all exceptions that can be raised in the Authentication module."""

class UserNotFoundException(Exception):
    """Exception to be raised when a user cannot be located in the database."""
    def __init__(self):
        super().__init__(
            "User not found."
        )

class InvalidCredentialsException(Exception):
    """Exception to be raised when invalid credentials are input for a user."""
    def __init__(self):
        super().__init__(
            "Invalid username or password."
        )

class DisabledUserException(Exception):
    """Exception to be raise when a user is disabled."""
    def __init__(self):
        super().__init__(
            "User disabled. Please re-authenticate for a new token."
        )

class InvalidTokenException(Exception):
    """Exception to be thrown when an invalid token is passed."""
    def __init__(self):
        super().__init__(
            "Shame on you. Invalid token."
        )

class DuplicateUserException(Exception):
    """Exception to be thrown during user creation of one of the input fields is already being used by another user."""
    def __init__(self, msg: str = "One of those fields is being used by another user. Please try again."):
        super().__init__(
            f"{msg}"
        )

class InvalidUserInputPropertyException(Exception):
    def __init__(self, msg: str = "Invalid input for username, email, or password. Please ensure that there are no spaces."):
        super().__init__(
            f"{msg}"
        )