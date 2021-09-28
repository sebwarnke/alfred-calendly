#!/usr/bin/python
# encoding: utf-8

import unittest
from mock import patch, Mock
import constants as c
from controller import Controller

EVENT_TYPE = "event_type_foo"


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

    def test_given_no_stats_when_get_event_types_then_empty_list_returns(self):
        # Given, nothing
        controller = Controller(self.mock_wf)

        # When
        event_types = controller.get_ordered_event_types()

        # Then
        self.assertDictEqual(event_types, {})

    def test_given_no_event_types_when_get_event_types_then_empty_list_returns(self):
        # Given, nothing
        controller = Controller(self.mock_wf)

        # When
        event_types = controller.get_ordered_event_types()

        # Then
        self.assertDictEqual(event_types, {})


if __name__ == "__main__":
    unittest.main()