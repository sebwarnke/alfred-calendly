import unittest
from mock import Mock
from mock import patch
from calendly_client import CalendlyClient

import constants as c

class CalendlyClientTest(unittest.TestCase):

    @patch("workflow.web.post")
    def test_when_authorize_returns_200_then_dict_with_tokens_is_returned(self, mock_web_post):

        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.json.return_value = {
          "token_type": "Bearer",
          "expires_in": 7200,
          "created_at": 1548689183,
          "refresh_token": "b77a76ffce83d3bc20531ddfa76704e584f0ee963f6041b8bfc70c91373267d5",
          "access_token": "ab32b480a9a755bd26421bc7e24e65dc055b039a3cf58430a5c5814a63c01d5a",
          "scope": "default",
          "owner": "https://api.calendly.com/users/EBHAAFHDCAEQTSEZ",
          "organization": "https://api.calendly.com/organizations/EBHAAFHDCAEQTSEZ"
        }

        mock_web_post.return_value = response_mock

        calendly_client = CalendlyClient("foo", "bar", "baz")
        r = calendly_client.authorize("code")

        assert r.get(c.ACCESS_TOKEN) == "ab32b480a9a755bd26421bc7e24e65dc055b039a3cf58430a5c5814a63c01d5a"
        assert r.get(c.REFRESH_TOKEN) == "b77a76ffce83d3bc20531ddfa76704e584f0ee963f6041b8bfc70c91373267d5"

    @patch("workflow.web.post")
    def test_when_authorize_returns_401_then_dict_with_tokens_is_returned(self, mock_web_post):
        response_mock = Mock()
        response_mock.status_code = 401

        mock_web_post.return_value = response_mock

        calendly_client = CalendlyClient("foo", "bar", "baz")
        r = calendly_client.authorize("code")

        assert r is None


if __name__ == "__main__":
    unittest.main()