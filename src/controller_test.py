#!/usr/bin/python
# encoding: utf-8

import unittest

from mock import patch, Mock

import constants as c
from controller import Controller

EVENT_TYPE = "event_type_foo"

THREE_EVENT_TYPES = [
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
        "active": True,
        "scheduling_url": "s3"
    }
]

EVENT_STATS = {
    "u3": 13,
    "u2": 42
}

THREE_EVENT_TYPES_SORTED = [
    {
        "uri": "u2",
        "active": True,
        "scheduling_url": "s2"
    },
    {
        "uri": "u3",
        "active": True,
        "scheduling_url": "s3"
    },
    {
        "uri": "u1",
        "active": True,
        "scheduling_url": "s1"
    }
]


class ControllerTest(unittest.TestCase):

    def setUp(self):
        self.mock_wf = Mock()
        self.mock_wf.get_password.return_value = "access_token"

    @patch("calendly_client.CalendlyClient.create_link")
    def test_given_no_stats_when_create_single_use_link_then_count_is_one(self, mock_create_link):
        # Given, nothing
        mock_create_link.return_value = "a_link"

        self.mock_wf.settings = {}
        controller = Controller(self.mock_wf)

        # When
        controller.create_single_use_link(EVENT_TYPE)

        # Then
        event_count = self.mock_wf.settings[c.CONF_EVENT_STATS][EVENT_TYPE]
        self.assertEquals(event_count, 1)

    @patch("calendly_client.CalendlyClient.create_link")
    def test_given_stats_exist_when_create_single_use_link_then_count_is_one(self, mock_create_link):
        # Given
        mock_create_link.return_value = "a_link"
        self.mock_wf.settings = {
            c.CONF_EVENT_STATS: {"foo": 42}
        }
        controller = Controller(self.mock_wf)

        # When
        controller.create_single_use_link(EVENT_TYPE)

        # Then
        event_count = self.mock_wf.settings[c.CONF_EVENT_STATS][EVENT_TYPE]
        self.assertEquals(event_count, 1)

    @patch("calendly_client.CalendlyClient.create_link")
    def test_given_event_type_exists_in_stats_when_create_single_use_link_then_count_increments(self, mock_create_link):
        # Given
        mock_create_link.return_value = "a_link"
        self.mock_wf.settings = {
            c.CONF_EVENT_STATS: {EVENT_TYPE: 42}
        }
        controller = Controller(self.mock_wf)

        # When
        controller.create_single_use_link(EVENT_TYPE)

        # Then
        event_count = self.mock_wf.settings[c.CONF_EVENT_STATS][EVENT_TYPE]
        self.assertEquals(event_count, 43)

    @patch("calendly_client.CalendlyClient.get_all_event_types_of_user")
    def test_given_no_event_types_when_get_event_types_then_empty_list_returns(self, mock_get_all_event_types_of_user):
        # Given, nothing
        mock_get_all_event_types_of_user.return_value = []
        self.mock_wf.settings = {
            c.CONF_EVENT_STATS: None
        }
        controller = Controller(self.mock_wf)

        # When
        event_types = controller.get_ordered_event_types("a_user")

        # Then
        self.assertListEqual(event_types, [])

    @patch("calendly_client.CalendlyClient.get_all_event_types_of_user")
    def test_given_event_types_but_no_stats_when_get_ordered_event_types_then_original_list_returns(self, mock_get_all_event_types_of_user):
        mock_get_all_event_types_of_user.return_value = THREE_EVENT_TYPES
        self.mock_wf.settings = {
            c.CONF_EVENT_STATS: None
        }

        controller = Controller(self.mock_wf)

        # When
        event_types = controller.get_ordered_event_types("a_user")

        self.assertListEqual(event_types, THREE_EVENT_TYPES)

    @patch("calendly_client.CalendlyClient.get_all_event_types_of_user")
    def test_given_event_types_and_stats_when_get_ordered_event_types_then_ordered_list_returns(self, mock_get_all_event_types_of_user):
        mock_get_all_event_types_of_user.return_value = THREE_EVENT_TYPES
        self.mock_wf.settings = {
            c.CONF_EVENT_STATS: EVENT_STATS
        }

        controller = Controller(self.mock_wf)

        # When
        event_types = controller.get_ordered_event_types("a_user")

        # Than
        ''' For the sake of the test, remove the event_stats attribute from the list items under test'''
        for item in event_types:
            if "event_stats" in item:
                del item["event_stats"]

        self.assertListEqual(event_types, THREE_EVENT_TYPES_SORTED)


if __name__ == "__main__":
    unittest.main()