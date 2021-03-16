import unittest
from mock import Mock
from mock import patch
from calendly_client import CalendlyClient
from calendly_client import active_filter as ACTIVE_FILTER

import constants as c

RESPONSE_INTROSPECT_TRUE = {
    "active": True
}

RESPONSE_INTROSPECT_FALSE = {
    "active": False
}

RESPONSE_AUTHORIZE = {
    "refresh_token": "b77a76ffce83d3bc20531ddfa76704e584f0ee963f6041b8bfc70c91373267d5",
    "access_token": "ab32b480a9a755bd26421bc7e24e65dc055b039a3cf58430a5c5814a63c01d5a"
}

RESPONSE_GET_EVENT_TYPES_1 = {
    "collection": [
        {
            "uri": "u1",
            "active": True,
            "scheduling_url": "s1"
        },
        {
            "uri": "u2",
            "active": True,
            "scheduling_url": "s2"
        },
        {
            "uri": "u3",
            "active": False,
            "scheduling_url": "s3"
        }
    ],
    "pagination": {
        "count": 1,
        "next_page": "https://api.calendly.com/event_types?count=20&page_token=A_TOKEN321&user=https%3A%2F%2Fapi.calendly.com%2Fusers%2ABC"
    }
}

RESPONSE_GET_EVENT_TYPES_2 = {
    "collection": [
        {
            "uri": "u4",
            "active": True,
            "scheduling_url": "s4"
        },
        {
            "uri": "u5",
            "active": True,
            "scheduling_url": "s5"
        },
        {
            "uri": "u6",
            "active": False,
            "scheduling_url": "s6"
        }
    ],
    "pagination": {
        "count": 1,
        "next_page": None
    }
}


class CalendlyClientTest(unittest.TestCase):
    calendly_client = None

    def setUp(self):
        self.calendly_client = CalendlyClient("foo", "bar", "baz")

    @patch("workflow.web.post")
    def test_when_authorize_returns_200_then_dict_with_tokens_is_returned(self, mock_web_post):
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.json.return_value = RESPONSE_AUTHORIZE

        mock_web_post.return_value = response_mock

        r = self.calendly_client.authorize("code")

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

    @patch("workflow.web.post")
    def test_when_introspect_returns_200_then_value_of_active_is_returned(self, mock_web_post):
        response_mock = Mock()
        response_mock.status_code = 200

        response_mock.json.return_value = RESPONSE_INTROSPECT_TRUE
        mock_web_post.return_value = response_mock
        r_true = self.calendly_client.introspect("access_token")
        assert r_true is True

        response_mock.json.return_value = RESPONSE_INTROSPECT_FALSE
        mock_web_post.return_value = response_mock
        r_false = self.calendly_client.introspect("access_token")
        assert r_false is False

    @patch("workflow.web.get")
    def test_when_get_event_types_returns_200_then_event_types_are_returned(self, mock_web_get):
        response_mock = Mock()
        response_mock.status_code = 200

        response_mock.json.return_value = RESPONSE_GET_EVENT_TYPES_1
        mock_web_get.return_value = response_mock

        r = self.calendly_client.get_event_types_of_user("user", "access_tocken")

        expected = {
            "collection": [
                {
                    "uri": "u1",
                    "active": True,
                    "scheduling_url": "s1"
                },
                {
                    "uri": "u2",
                    "active": True,
                    "scheduling_url": "s2"
                },
                {
                    "uri": "u3",
                    "active": False,
                    "scheduling_url": "s3"
                }
            ],
            "pagination": {
                "count": 1,
                "next_page": "p2"
            }
        }

        self.assertDictEqual(r, expected)

    @patch("calendly_client.CalendlyClient.get_event_types_of_user")
    def test_when_get_all_event_types_then_all_event_types_are_returned(self, get_event_types_of_user):

        get_event_types_of_user.side_effect = [RESPONSE_GET_EVENT_TYPES_1, RESPONSE_GET_EVENT_TYPES_2]

        r = self.calendly_client.get_all_event_types_of_user("user", "access_tocken")

        expected = [
            {
                "uri": "u1",
                "active": True,
                "scheduling_url": "s1"
            },
            {
                "uri": "u2",
                "active": True,
                "scheduling_url": "s2"
            },
            {
                "uri": "u3",
                "active": False,
                "scheduling_url": "s3"
            },
            {
                "uri": "u4",
                "active": True,
                "scheduling_url": "s4"
            },
            {
                "uri": "u5",
                "active": True,
                "scheduling_url": "s5"
            },
            {
                "uri": "u6",
                "active": False,
                "scheduling_url": "s6"
            }
        ]

        assert all(item in expected for item in r)

    @patch("calendly_client.CalendlyClient.get_event_types_of_user")
    def test_when_get_all_active_event_types_then_active_event_types_are_returned(self, get_event_types_of_user):

        get_event_types_of_user.side_effect = [RESPONSE_GET_EVENT_TYPES_1, RESPONSE_GET_EVENT_TYPES_2]

        r = self.calendly_client.get_all_event_types_of_user("user", "access_tocken", the_filter=ACTIVE_FILTER)

        expected = [
            {
                "uri": "u1",
                "active": True,
                "scheduling_url": "s1"
            },
            {
                "uri": "u2",
                "active": True,
                "scheduling_url": "s2"
            },
            {
                "uri": "u4",
                "active": True,
                "scheduling_url": "s4"
            },
            {
                "uri": "u5",
                "active": True,
                "scheduling_url": "s5"
            }
        ]

        self.assertListEqual(r, expected)


if __name__ == "__main__":
    unittest.main()
