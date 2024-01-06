from enum import Enum


class Order(str, Enum):
    """
    Order enum to be used in search
    """

    ASC = "asc"
    DESC = "desc"
