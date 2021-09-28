#!/usr/bin/python
# encoding: utf-8
from calendly_client import CalendlyClient, CalendlyClientException
import constants as c


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


    def get_ordered_event_types(self):
        return None


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