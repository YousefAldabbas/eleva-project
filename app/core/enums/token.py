from enum import Enum


class Token(str, Enum):
    """
    Enum class for token
    """

    ACCESS = "access"
    REFRESH = "refresh"
