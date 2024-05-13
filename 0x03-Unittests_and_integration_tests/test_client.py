#!/usr/bin/env python3
"""
Defines class for testing GithubOrgClient.
"""
from client import GithubOrgClient
import unittest
from parameterized import parameterized
from unittest.mock import patch


class TestGithubOrgClient(unittest.TestCase):
    """
    Tests the methods of the class TestGithubOrgClient.
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self,
                 org: str,
                 mock_get_json):
        """
        Tests the method org of GithubOrgClient.
        """
        client = GithubOrgClient(org)
        sample_payload = {"result": "result"}
        mock_get_json.return_value = sample_payload
        call1 = client.org
        call2 = client.org
        mock_get_json.assert_called_once_with(client.ORG_URL.format(org=org))
        self.assertEqual(call1, call2)
