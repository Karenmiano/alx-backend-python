#!/usr/bin/env python3
""""Defines a function make_multiplier"""
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """Returns a function that multiplies a float by multiplier"""
    def inner_multiplier(inner: float) -> float:
        return inner * multiplier
    return inner_multiplier
