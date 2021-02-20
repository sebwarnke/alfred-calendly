#!/usr/bin/python
# encoding: utf-8

import sys
import os
import webbrowser
from workflow import Workflow3, web
from urllib2 import HTTPError
from api_helper import reset_workflow_config

import constants as c

log = None


def store_in_clipboard(clip):
    command = "printf %s | pbcopy" % clip.strip()
    os.system(command)


def get_single_use_link(owner, access_token):
    log.debug("in: get_single_use_link")
    try:
        response = web.post(
            url="%s%s" % (c.CALENDLY_API_BASE_URL, c.CALENDLY_SCHEDULING_LINK_URI),
            headers={
                "Authorization": "Bearer %s" % access_token,
            },
            data={
                "max_event_count": 1,
                "owner": owner,
                "owner_type": "EventType"
            }
        )
        log.debug("Response Status Code: %d" % response.status_code)
        response.raise_for_status()

        if response.status_code == 201:
            return response.json()["resource"]["booking_url"]
        else:
            raise Exception("Error whilst getting single use link.")
    except HTTPError:
        raise Exception("Error whilst getting single use link.")


def increment_usage_counter(uri):
    counterwf.settings.get(c.CONF_SINGLE_USE_LINK_COUNTER)


def main(wf):
    # type: (Workflow3) -> None

    user_input = ''.join(wf.args)

    command = user_input.split()[0]
    query = user_input[len(command) + 1:]

    log.debug("%s : %s" % (command, query))

    access_token = wf.get_password(c.ACCESS_TOKEN)

    if command == c.CMD_SINGLE_USE_LINK:
        try:
            single_use_link = get_single_use_link(query, access_token)
            increment_usage_counter(query)
            store_in_clipboard(single_use_link)
            print("Link stored in Clipboard: %s" % single_use_link)
        except Exception as e:
            print(e.message)
    elif command == c.CMD_BROWSE_URL:
        webbrowser.open(query)
    elif command == c.CMD_LOGOUT:
        try:
            reset_workflow_config(wf)
        finally:
            print("All local data deleted.")


if __name__ == u"__main__":
    wf = Workflow3()
    log = wf.logger

    sys.exit(wf.run(main))
