from enum import Enum


class Order(str, Enum):
    ASC = "asc"
    DESC = "desc"
