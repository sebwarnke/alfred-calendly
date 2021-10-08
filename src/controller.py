#!/usr/bin/python
# encoding: utf-8
import constants as c
from calendly_client import CalendlyClient, CalendlyClientException
from calendly_client import active_filter as ACTIVE_FILTER


class Controller:
    calendly_client = None

    def __init__(self, wf):
        access_token = wf.get_password(c.ACCESS_TOKEN)
        self.calendly_client = CalendlyClient(access_token)
        self.stats = Stats(wf)

    def create_single_use_link(self, event_type):
        try:
            link = self.calendly_client.create_link(event_type, 1)
            self.stats.increment(event_type)

        except CalendlyClientException:
            pass

    def get_ordered_event_types(self, user):

        ordered_event_types = []

        unordered_event_types = self.calendly_client.get_all_event_types_of_user(user, the_filter=ACTIVE_FILTER)
        if not unordered_event_types:
            return []

        event_stats = self.stats.get_stats()
        if not event_stats:
            return unordered_event_types

        for event_stats_item in event_stats.items():
            for i in range(len(unordered_event_types)):
                needle = unordered_event_types[i]
                if needle["uri"] == event_stats_item[0]:
                    unordered_event_types[i]["event_stats"] = event_stats_item[1]

        ordered_event_types = sorted(unordered_event_types, key=lambda event_type: event_type["event_stats"] if "event_stats" in event_type else None, reverse=True)

        return ordered_event_types


class Stats:

    def __init__(self, wf):
        event_stats = wf.settings.get(c.CONF_EVENT_STATS)
        if event_stats is None:
            wf.settings[c.CONF_EVENT_STATS] = {}

        self.wf = wf

    def increment(self, event_type):
        if event_type in self.wf.settings[c.CONF_EVENT_STATS]:
            current_count = self.wf.settings[c.CONF_EVENT_STATS][event_type]
            self.wf.settings[c.CONF_EVENT_STATS][event_type] = current_count + 1
        else:
            self.wf.settings[c.CONF_EVENT_STATS][event_type] = 1

    def get_stats(self):
        return self.wf.settings[c.CONF_EVENT_STATS]


