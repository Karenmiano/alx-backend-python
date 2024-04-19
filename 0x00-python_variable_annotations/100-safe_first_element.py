#!/usr/bin/env python3
"""
Defines a function safe_first_element
"""
from typing import Sequence, Any, Union


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """Returns the first element of a sequence or None."""
    if lst:
        return lst[0]
    else:
        return None
