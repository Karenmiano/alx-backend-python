#!/usr/bin/env python3
"""
Defines the classes for testing functions in the
module utils.py.
"""
from utils import (
    access_nested_map,
    get_json,
    memoize
    )
from functools import lru_cache
from parameterized import parameterized
import unittest
from unittest.mock import patch, Mock
from typing import Any, Sequence, Mapping, Dict


class TestAccessNestedMap(unittest.TestCase):
    """
    Class for testing the access_nested_map function.

    Methods:
        test_access_nested_map
        test_access_nested_map_exception
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


class TestGetJson(unittest.TestCase):
    """
    Class for testing get_json from utils.

    Methods:
        test_get_json
    """
    @parameterized.expand([
       ("http://example.com", {"payload": True}),
       ("http://holberton.io", {"payload": False}),
    ])
    @patch('utils.requests.get')
    def test_get_json(
            self,
            test_url: str,
            test_payload: Dict,
            mock_get) -> None:
        """
        Test the get_json function.

        Asserts:
            That requests is called with the right url.
            Function returns faked response.
        """
        mock_response = Mock()
        response_dict = test_payload
        mock_response.json.return_value = response_dict
        mock_get.return_value = mock_response

        response = get_json(test_url)
        mock_get.assert_called_once_with(test_url)
        self.assertEqual(response, response_dict)


class TestMemoize(unittest.TestCase):
    """
    Class for testing memoized method a_property

    Methods:
        test_memoize
    """

    def test_memoize(self):
        """
        Tests the memoized method a_property.

        Asserts:
            That the method returns the same value when called
            more than once.
            Helper method a_method is only called once.(Memoization)
        """
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(
                TestClass,
                'a_method',
                return_value=42) as mock_method:
            test_obj = TestClass()
            val1 = test_obj.a_property
            val2 = test_obj.a_property
            self.assertEqual(val1, val2)
            mock_method.assert_called_once()


if __name__ == '__main__':
    unittest.main()
