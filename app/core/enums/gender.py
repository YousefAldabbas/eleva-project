from enum import Enum


class Gender(str, Enum):
    """
    Enum class for gender
    """

    MALE = "Male"
    FEMALE = "Female"
    NOT_SPECIFIED = "Not Specified"
