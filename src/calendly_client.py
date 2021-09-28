#!/usr/bin/python
# encoding: utf-8

import re

import constants as c
from workflow import Workflow3, web

log = Workflow3().logger


def active_filter(event_type):
    return event_type.get("active")


class CalendlyClient:
    def __init__(self,access_token):
        self.access_token = access_token

    def get_event_types_of_user(self, user, page_token=None):
        log.debug("in: get_event_types_of_user")

        request_params = {
            "user": user
        }
        if page_token is not None:
            request_params["page_token"] = page_token

        response = web.get(
            url="%s%s" % (c.CALENDLY_API_BASE_URL, c.CALENDLY_EVENT_TYPES_URI),
            headers={
                "Authorization": "Bearer %s" % self.access_token,
            },
            params=request_params
        )
        response.raise_for_status()

        if response.status_code == 200:
            return response.json()
        else:
            log.error(
                "Getting Event Types failed. Calendly returned status [%s]. Response payload below." % response.status_code)
            log.error(response.json())
            return None

    def get_all_event_types_of_user(self, user, the_filter=None):
        log.debug("in: get_all_event_types_of_user")

        event_types = []
        page_token = None

        while True:
            r = self.get_event_types_of_user(user, page_token)
            next_page_uri = r["pagination"]["next_page"]

            event_types.extend(r.get("collection"))

            if next_page_uri is None:
                break

            match_page_token = re.search(".*page_token=([^&]*)", next_page_uri)
            if match_page_token is not None:
                page_token = match_page_token.group(1)

        if the_filter is not None:
            event_types = filter(the_filter, event_types)

        return event_types

    def get_current_user(self):
        log.debug("in: get_current_user")
        response = web.get(
            url="%s%s" % (c.CALENDLY_API_BASE_URL, c.CALENDLY_CURRENT_USER_URI),
            headers={
                "Authorization": "Bearer %s" % self.access_token,
            }
        )
        response.raise_for_status()

        if response.status_code == 200:
            return response.json()["resource"]["uri"]
        else:
            log.error(
                "Getting current user failed. Calendly returned status [%s]. Response payload below." % response.status_code)
            log.error(response.json())
            return None

    def create_link(self, event_type, event_count):
        log.debug("in: create_link")
        log.debug("Event Type: [%s], Max. Event Count: [%d]" % (event_type, event_count))

        response = web.post(
            url="%s%s" % (c.CALENDLY_API_BASE_URL, c.CALENDLY_SCHEDULING_LINK_URI),
            headers={
                "Authorization": "Bearer %s" % self.access_token,
            },
            data={
                "max_event_count": event_count,
                "owner": event_type,
                "owner_type": "EventType"
            }
        )

        if response.status_code != 201:
            log.error(
                "Creating a link failed. Calendly returned status [%s]. Response payload below." % response.status_code)
            log.error(response.json())
            raise CalendlyClientException

        return response.json()["resource"]["booking_url"]


class CalendlyClientException(Exception):
    pass
