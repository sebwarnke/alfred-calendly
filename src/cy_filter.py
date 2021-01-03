#!/usr/bin/python
# encoding: utf-8

import sys

from workflow import Workflow3, PasswordNotFound, web
from urllib2 import HTTPError
import constants as c

log = None


def introspect_and_conditionally_refresh_access_token():
    try:
        client_id = wf.get_password(c.CLIENT_ID)
        client_secret = wf.get_password(c.CLIENT_SECRET)
        access_token = wf.get_password(c.ACCESS_TOKEN)
        refresh_token = wf.get_password(c.REFRESH_TOKEN)

        log.debug("Introspecting Access Token")
        response = web.post(
            url="%s%s" % (c.CALENDLY_AUTH_BASE_URL, c.CALENDLY_INTROSPECT_URI),
            data={
                "client_id": client_id,
                "client_secret": client_secret,
                "token": access_token
            }
        )
        response.raise_for_status()

        response_json = response.json()
        if response_json["active"] is False:
            log.debug("Refreshing Access Token.")
            response = web.post(
                url="%s%s" % (c.CALENDLY_AUTH_BASE_URL, c.CALENDLY_TOKEN_URI),
                data={
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "refresh_token": refresh_token,
                    "grant_type": "refresh_token"
                }
            )
            response.raise_for_status()

            if response.status_code == 200:
                response_json = response.json()
                wf.save_password(c.ACCESS_TOKEN, response_json["access_token"])
                wf.save_password(c.REFRESH_TOKEN, response_json["refresh_token"])

    except PasswordNotFound:
        wf.add_item(
            title="No Calendly Client registered yet.",
            subtitle="Use 'cya' to start authentication flow.",
            valid=False
        )
        wf.send_feedback()
        return 0

    except HTTPError:
        wf.add_item(
            title="Authentication API Error",
            subtitle="Calendly returned an error whilst checking your OAuth Access Token.",
            valid=False
        )
        wf.send_feedback()
        return 0


def get_current_user():
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
    introspect_and_conditionally_refresh_access_token()
    current_user = get_current_user()
    return get_event_types_for_user(current_user)


def refresh_event_types_conditionally():
    if wf.cached_data_age(c.CACHE_EVENT_TYPES) > 300:
        wf.cache_data(c.CACHE_EVENT_TYPES, get_event_types_for_current_user())


def get_search_key_for_event_types(event_type):
    elements = [
        event_type['name'],
        event_type['scheduling_url']
    ]
    return u' '.join(elements)

def main(wf):
    # type: (Workflow3) -> None

    user_input = wf.args[0]
    command = query = ""
    if len(user_input) > 0:
        log.debug("Input: %s" % user_input)
        command = user_input.split()[0]
        query = user_input[len(command) + 1:]

    if command == "":
        wf.add_item(
            title="Create Single-Use-Link",
            subtitle="Copies the Single-Use-Link to the Clipboard.",
            autocomplete="%s " % c.CMD_SINGLE_USE_LINK,
            valid=False
        )
        wf.send_feedback()
    elif command == c.CMD_SINGLE_USE_LINK:
        try:
            event_types = wf.cached_data(c.CACHE_EVENT_TYPES, get_event_types_for_current_user, max_age=0)

            if query != "":
                event_types = wf.filter(query, event_types, key=get_search_key_for_event_types, min_score=20)

            for event_type in event_types:
                wf.add_item(
                    title=event_type["name"],
                    subtitle=event_type["scheduling_url"],
                    valid=True,
                    arg="%s %s" % (c.CMD_SINGLE_USE_LINK, event_type["uri"])
                )
        except Exception as e:
            wf.add_item(
                title="API Error",
                subtitle=e.message,
                valid=False
            )
        finally:
            wf.send_feedback()
            refresh_event_types_conditionally()


if __name__ == '__main__':
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main))
