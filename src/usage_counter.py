#!/usr/bin/python
# encoding: utf-8

import json
import constants as c


def increment_counter_for_uri_in_dict(uri, settings_dict):
    counter = settings_dict[uri]

    if counter is None:
        new_counter = 1
    else:
        new_counter = counter + 1
    settings_dict[uri] = new_counter

    return settings_dict


def get_counter_for_uri(uri, settings_dict):
    counter = settings_dict[uri]

    if counter is None:
        counter = 0

    return counter


class UsageCounter:

    wf = None
    settings_dict = None

    def __init__(self, wf):
        self.wf = wf

        settings_json = wf.settings.get(c.CONF_SINGLE_USE_LINK_COUNTER)

        if settings_json is None or settings_json == "":
            settings_json = "{}"
            self.wf.settings[c.CONF_SINGLE_USE_LINK_COUNTER] = settings_json

        self.settings_dict = json.loads(settings_json)

    def increment_for_uri(self, uri):
        updated_dict = increment_counter_for_uri_in_dict(uri, self.settings_dict)
        self.wf.settings[c.CONF_SINGLE_USE_LINK_COUNTER] = json.dumps(updated_dict)
