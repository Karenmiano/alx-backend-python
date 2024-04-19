#!/usr/bin/env python3
"""
Defines a function safely_get_value
"""
from typing import Mapping, Any, Union, TypeVar

T = TypeVar('T')
ret = Union[Any, T]
Def = Union[T, None]


def safely_get_value(dct: Mapping, key: Any, default: Def = None) -> ret:
    """
    Returns the value of a key in a dictionary
    """
    if key in dct:
        return dct[key]
    else:
        return default
