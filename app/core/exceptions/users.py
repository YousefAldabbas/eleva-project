from fastapi import status


class UserAlreadyExists(Exception):
    """Exception raised when user already exists"""

    def __init__(self):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.message = "User already exists"
        super().__init__(self.status_code, self.message)


class UserNotFound(Exception):
    """Exception raised when user not found"""

    def __init__(self):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.message = "User not found"
        super().__init__(self.status_code, self.message)


class UserNotAuthorized(Exception):
    """Exception raised when user not authorized"""

    def __init__(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.message = "User not authorized"
        super().__init__(self.status_code, self.message)


class UserNotAuthenticated(Exception):
    """Exception raised when user not authenticated"""

    def __init__(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.message = "User not authenticated"
        super().__init__(self.status_code, self.message)


class UserEmailAlreadyExists(Exception):
    """Exception raised when user email already exists"""

    def __init__(self):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.message = "Email already exists, please use another one"
        super().__init__(self.status_code, self.message)
