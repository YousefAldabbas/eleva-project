from enum import Enum
from typing import Any


def is_enum_value(value: Any, enum_class: Enum) -> bool:
    """Check if value is a member of enum class"""
    return any(value == member.value for member in enum_class)
