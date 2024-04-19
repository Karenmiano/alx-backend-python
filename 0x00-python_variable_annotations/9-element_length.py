#!/usr/bin/env python3
"""
Defines a function element_length
"""
from typing import Sequence, Tuple, Iterable, List


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """Returns a list of tuples of iterables with their length."""
    return [(i, len(i)) for i in lst]
