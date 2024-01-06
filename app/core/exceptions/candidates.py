from fastapi import status


class CandidateAlreadyExists(Exception):
    """Exception raised when candidate already exists"""

    def __init__(self):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.message = "Candidate already exists"
        super().__init__(self.status_code, self.message)


class CandidateNotFound(Exception):
    """Exception raised when candidate not found"""

    def __init__(self):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.message = "Candidate not found"
        super().__init__(self.status_code, self.message)


class CandidateNotAuthorized(Exception):
    """Exception raised when candidate not authorized"""

    def __init__(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.message = "Candidate not authorized"
        super().__init__(self.status_code, self.message)


class CandidateNotAuthenticated(Exception):
    """Exception raised when candidate not authenticated"""

    def __init__(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.message = "Candidate not authenticated"
        super().__init__(self.status_code, self.message)


class CandidateEmailAlreadyExists(Exception):
    """Exception raised when candidate email already exists"""

    def __init__(self):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.message = "Email already exists, please use another one"
        super().__init__(self.status_code, self.message)
