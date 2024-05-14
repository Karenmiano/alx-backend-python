#!/usr/bin/env python3
"""
Defines class for testing GithubOrgClient.
"""
from client import GithubOrgClient
import unittest
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, PropertyMock, Mock
from fixtures import TEST_PAYLOAD


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


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    [
        (
            TEST_PAYLOAD[0][0],
            TEST_PAYLOAD[0][1],
            TEST_PAYLOAD[0][2],
            TEST_PAYLOAD[0][3],
        ),
    ]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Does an Integration test of GithubOrgClient.
    """

    @classmethod
    def setUpClass(cls):
        """
        Begins the patch for 'utils.requests.get'
        Sets up a GithubOrgClient object.
        """
        cls.client = GithubOrgClient("google")
        cls.get_patcher = patch('requests.get')
        cls.mocked_get = cls.get_patcher.start()

        def side_effect(*args, **kwargs):
            """
            """
            url = args[0]
            mocked_response = Mock()
            if url == cls.org_payload["repos_url"]:
                mocked_response.json.return_value = cls.repos_payload
            else:
                mocked_response.json.return_value = cls.org_payload
            return mocked_response

        cls.mocked_get.side_effect = side_effect

    def test_public_repos(self):
        """
        Tests the method public_repos.
        """
        repos = self.client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """
        Tests public_repos with license argument.
        """
        repos = self.client.public_repos("apache-2.0")
        self.assertEqual(repos, self.apache2_repos)

    @classmethod
    def tearDownClass(cls):
        """
        Ends the patch for 'utils.requests.get'.
        """
        cls.get_patcher.stop()


if __name__ == '__main__':
    unittest.main()
