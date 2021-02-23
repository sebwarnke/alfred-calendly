#!/usr/bin/python
# encoding: utf-8

import sys
import constants as c
from workflow import Workflow3, web
from urllib2 import HTTPError

log = Workflow3().logger


class CalendlyClient:

    client_id = ""
    client_secret = ""
    redirect_uri = ""

    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    def authorize(self, code):
        response = web.post(
            url="%s%s" % (c.CALENDLY_AUTH_BASE_URL, c.CALENDLY_TOKEN_URI),
            data={
                "grant_type": "authorization_code",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "code": code,
                "redirect_uri": self.redirect_uri
            }
        )
        response.raise_for_status()

        if response.status_code == 200:
            return {
                c.ACCESS_TOKEN: response.json()["access_token"],
                c.REFRESH_TOKEN: response.json()["refresh_token"]
            }
        else:
            return None

    """Introspects the Token. Returns True only when request succeeded and token is still active"""
    def introspect(self, access_token):
        response = web.post(
            url="%s%s" % (c.CALENDLY_AUTH_BASE_URL, c.CALENDLY_INTROSPECT_URI),
            data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "token": access_token
            }
        )
        response.raise_for_status()

        if response.status_code != 200:
            return False
        else:
            return response.json()["active"]

    def refresh_token(self, refresh_token):
        response = web.post(
            url="%s%s" % (c.CALENDLY_AUTH_BASE_URL, c.CALENDLY_TOKEN_URI),
            data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "refresh_token": refresh_token,
                "grant_type": "refresh_token"
            }
        )
        response.raise_for_status()
        return response



    def create_scheduling_link(self):
        pass

    def get_event_types(self, access_token):
        response = web.get(
            url="%s%s" % (c.CALENDLY_API_BASE_URL, c.CALENDLY_CURRENT_USER_URI),
            headers={
                "Authorization": "Bearer %s" % access_token,
            }
        )
        response.raise_for_status()

    def get_current_user(self):
        pass
