#!/usr/bin/python
# encoding: utf-8

import sys

from workflow import Workflow3, PasswordNotFound, ICON_ACCOUNT
from workflow.background import run_in_background, is_running
from urllib2 import HTTPError
import constants as c

log = None


def get_search_key_for_event_types(event_type):
    elements = [
        event_type['name'],
        event_type['scheduling_url']
    ]
    return u' '.join(elements)


def maintain_oauth_access():
    cmd = ['/usr/bin/python', wf.workflowfile('cy_maintain_access_in_background.py')]
    run_in_background('maintain_oauth_access', cmd)


def preload_event_types_regularly():
    if not wf.cached_data_fresh(c.CACHE_EVENT_TYPES, max_age=300):
        log.debug("Event Types Cache expired.")
        cmd = ['/usr/bin/python', wf.workflowfile('cy_preload_event_types.py')]
        run_in_background('preload_event_types', cmd)
    else:
        log.debug("Event Types in Cache still fresh.")


def verify_configuration_exists():
    wf.get_password(c.CLIENT_ID)
    wf.get_password(c.CLIENT_SECRET)
    wf.get_password(c.REFRESH_TOKEN)
    wf.get_password(c.ACCESS_TOKEN)


def main(wf):
    # type: (Workflow3) -> None

    try:
        verify_configuration_exists()
    except PasswordNotFound:
        wf.add_item(
            title="Before you can start, run 'cya'",
            subtitle="You need to authenticate the workflow towards Calendly. Run 'cya' and follow the instructions.",
            valid=False,
            icon=ICON_ACCOUNT
        )
        wf.send_feedback()
        return 0

    maintain_oauth_access()
    preload_event_types_regularly()

    user_input = wf.args[0]
    command = query = ""
    if len(user_input) > 0:
        log.debug("Input: %s" % user_input)
        command = user_input.split()[0]
        query = user_input[len(command) + 1:]

    if command == c.CMD_SINGLE_USE_LINK:
        event_types = wf.cached_data(c.CACHE_EVENT_TYPES, None, max_age=0)

        if query != "":
            event_types = wf.filter(query, event_types, key=get_search_key_for_event_types, min_score=20)

        if len(event_types) == 0:
            wf.add_item(
                title="No Event Types found.",
                subtitle="... no events you could miss, though.",
                valid=False
            )

        for event_type in event_types:
            wf.add_item(
                title=event_type["name"],
                subtitle=event_type["scheduling_url"],
                valid=True,
                arg="%s %s" % (c.CMD_SINGLE_USE_LINK, event_type["uri"])
            )
        wf.send_feedback()

    else:
        wf.add_item(
            title="Create Single-Use-Link",
            subtitle="Copies the Single-Use-Link to the Clipboard.",
            autocomplete="%s " % c.CMD_SINGLE_USE_LINK,
            valid=False
        )
        wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow3()
    log = wf.logger
    wf.settings["bar"] = "baz"
    sys.exit(wf.run(main))
