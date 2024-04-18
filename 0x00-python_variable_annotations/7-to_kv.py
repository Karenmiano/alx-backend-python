#!/usr/bin/env python3
"""
Defines function to_kv
"""
from typing import Tuple


def to_kv(k: str, v: int | float) -> Tuple[str, float]:
    """Returns a tuple of function arguments"""
    return (k, v**2)
