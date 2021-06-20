#!/usr/bin/python
# encoding: utf-8

import unittest

import constants as c
import controller
from workflow import Workflow3

EVENT_TYPE = "event_type_foo"


class ControllerTest(unittest.TestCase):
    wf = None

    def setUp(self):
        self.wf = Workflow3()
        self.wf.clear_settings()

    def test_given_no_stats_when_create_single_use_link_then_count_is_one(self):
        # Given, nothing

        # When
        controller.create_single_use_link(EVENT_TYPE)

        # Then
        event_count = self.wf.settings[c.CONF_EVENT_STATS][EVENT_TYPE]
        self.assertEquals(event_count, 1)

    def test_given_stats_exist_when_create_single_use_link_then_count_is_one(self):
        # Given
        self.wf.settings[c.CONF_EVENT_STATS] = {"foo": 42}

        # When
        controller.create_single_use_link(EVENT_TYPE)

        # Then
        event_count = self.wf.settings[c.CONF_EVENT_STATS][EVENT_TYPE]
        self.assertEquals(event_count, 1)

    def test_given_event_type_exists_in_stats_when_create_single_use_link_then_count_increments(self):
        # Given
        self.wf.settings[c.CONF_EVENT_STATS] = {EVENT_TYPE: 42}

        # When
        controller.create_single_use_link(EVENT_TYPE)

        # Then
        event_count = self.wf.settings[c.CONF_EVENT_STATS][EVENT_TYPE]
        self.assertEquals(event_count, 43)

    def test_given_no_stats_when_get_event_types_then_empty_list_returns(self):
        # Given, nothing

        # When
        event_types = controller.get_ordered_event_types()

        # Then
        self.assertDictEqual(event_types, {})

    def test_given_no_event_types_when_get_event_types_then_empty_list_returns(self):
        # Given, nothing

        # When
        event_types = controller.get_ordered_event_types()

        # Then
        self.assertDictEqual(event_types, {})

    def test_given_no_stats_when_get_event_types_then_empty_list_returns(self):
        # Given, nothing

        # When
        event_types = controller.get_ordered_event_types()

        # Then
        self.assertDictEqual(event_types, {})