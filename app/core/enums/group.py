from enum import Enum


class Group(str, Enum):
    """
    Enum class for group
    """

    USER = "user"
    CANDIDATE = "candidate"
