import unittest
from mock import Mock
from mock import patch
from calendly_client import CalendlyClient
from calendly_client import active_filter as ACTIVE_FILTER

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
        self.calendly_client = CalendlyClient("access_token")

    @patch("workflow.web.get")
    def test_when_get_event_types_returns_200_then_event_types_are_returned(self, mock_web_get):
        response_mock = Mock()
        response_mock.status_code = 200

        response_mock.json.return_value = RESPONSE_GET_EVENT_TYPES_1
        mock_web_get.return_value = response_mock

        r = self.calendly_client.get_event_types_of_user("user")

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
                "next_page": "https://api.calendly.com/event_types?count=20&page_token=A_TOKEN321&user=https%3A%2F%2Fapi.calendly.com%2Fusers%2ABC"
            }
        }

        self.assertDictEqual(r, expected)

    @patch("calendly_client.CalendlyClient.get_event_types_of_user")
    def test_when_get_all_event_types_then_all_event_types_are_returned(self, get_event_types_of_user):
        get_event_types_of_user.side_effect = [RESPONSE_GET_EVENT_TYPES_1, RESPONSE_GET_EVENT_TYPES_2]

        r = self.calendly_client.get_all_event_types_of_user("user")

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

        r = self.calendly_client.get_all_event_types_of_user("user", the_filter=ACTIVE_FILTER)

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
