# encoding: utf-8

from workflow import Workflow3, web
from urllib2 import HTTPError
import constants as c


def get_current_user():
    wf = Workflow3()
    log = wf.logger

    log.debug("in: get_current_user")
    try:
        access_token = wf.get_password(c.ACCESS_TOKEN)

        response = web.get(
            url="%s%s" % (c.CALENDLY_API_BASE_URL, c.CALENDLY_CURRENT_USER_URI),
            headers={
                "Authorization": "Bearer %s" % access_token,
            }
        )
        log.debug("Response Status Code: %d", response.status_code)
        response.raise_for_status()
        if response.status_code == 200:
            return response.json()["resource"]["uri"]
        else:
            raise Exception("Error whilst getting current user.")
    except HTTPError:
        raise Exception("Error whilst getting current user.")


def get_event_types_for_user(current_user_uri):
    wf = Workflow3()
    log = wf.logger

    log.debug("in: get_event_types_for_user")
    try:
        access_token = wf.get_password(c.ACCESS_TOKEN)
        response = web.get(
            url="%s%s" % (c.CALENDLY_API_BASE_URL, c.CALENDLY_EVENT_TYPES_URI),
            headers={
                "Authorization": "Bearer %s" % access_token,
            },
            params={
                "user": current_user_uri
            }
        )
        response.raise_for_status()

        if response.status_code == 200:
            return response.json()["collection"]
        else:
            raise Exception("Error whilst getting current user.")
    except HTTPError:
        raise Exception("Error whilst getting current user.")


def get_event_types_for_current_user():

    current_user = get_current_user()
    return get_event_types_for_user(current_user)