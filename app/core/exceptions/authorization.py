from fastapi import status


class InvalidCredentials(Exception):
    """Exception raised when user email already exists"""

    def __init__(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.message = "Invalid credentials"
        super().__init__(self.status_code, self.message)


class Unauthorized(Exception):
    """Exception raised when user email already exists"""

    def __init__(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.message = "You are not authorized to access this resource"
        super().__init__(self.status_code, self.message)


class InvalidTokenPayload(Exception):
    """Exception raised when user email already exists"""

    def __init__(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.message = "Invalid token payload"
        super().__init__(self.status_code, self.message)


class InvalidToken(Exception):
    """Exception raised when user email already exists"""

    def __init__(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.message = "Invalid token"
        super().__init__(self.status_code, self.message)
