#!/usr/bin/env python3
"""
Defines the class TestAccessNestedMap
"""
from utils import access_nested_map
from parameterized import parameterized
import unittest
from typing import Any, Sequence, Mapping


class TestAccessNestedMap(unittest.TestCase):
    """
    Class for testing the access_nested_map function.

    Methods:
        test_access_nested_map
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b",), 2),
    ])
    def test_access_nested_map(
            self,
            nested_map: Mapping,
            path: Sequence,
            accessed_val: Any) -> None:
        """
        Test the access_nested_map function

        Asserts:
            Asserts that the result of 'access_nested_map' is equal
            to accessed_val.
        """
        self.assertEqual(access_nested_map(nested_map, path), accessed_val)

    @parameterized.expand([
        ({}, ("a",), 'a'),
        ({"a": 1}, ("a", "b"), 'b'),
    ])
    def test_access_nested_map_exception(
            self,
            nested_map: Mapping,
            path: Sequence,
            msg: str) -> None:
        """
        Test the access_nested_map function's error handling

        Asserts:
            Asserts that a KeyError with 'msg' is raised if current
            nested_map is actually not a dict.
        """
        with self.assertRaisesRegex(KeyError, msg):
            access_nested_map(nested_map, path)


if __name__ == '__main__':
    unittest.main()
