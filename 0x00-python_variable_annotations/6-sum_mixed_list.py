#!/usr/bin/env python3
"""Defines function sum_mixed_list"""
from typing import List, Union


def sum_mixed_list(mxd_list: List[Union[int, str]]) -> float:
    """Returns the sum of integers and floats in a list"""
    return sum(mxd_list)
