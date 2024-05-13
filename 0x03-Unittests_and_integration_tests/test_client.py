#!/usr/bin/env python3
"""
Defines class for testing GithubOrgClient.
"""
from client import GithubOrgClient
import unittest
from parameterized import parameterized
from unittest.mock import patch, PropertyMock


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

    def test_public_repos_url(self):
        """
        Tests the property getter _public_repos_url.
        """
        with patch(
                'client.GithubOrgClient.org',
                new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "sample_repo_url"}
            client = GithubOrgClient('org')
            repos_url = client._public_repos_url
            self.assertEqual(repos_url, "sample_repo_url")

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        Tests the method public_repos.
        """
        with patch(
            'client.GithubOrgClient._public_repos_url',
            new_callable=PropertyMock,
        ) as mock_pru:
            mock_pru.return_value = "repos_url"
            mock_get_json.return_value = [
                {"name": "repo1"},
                {"name": "repo2"}
            ]

            client = GithubOrgClient('org')
            repos = client.public_repos()
            self.assertEqual(repos, ["repo1", "repo2"])
            client.public_repos()
            mock_get_json.assert_called_once_with("repos_url")
            mock_pru.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """Tests the has_license method."""
        client = GithubOrgClient('org')
        self.assertEqual(client.has_license(repo, license_key), expected)


if __name__ == '__main__':
    unittest.main()
