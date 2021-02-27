#!/usr/bin/python
# encoding: utf-8

import os
import sys
import webbrowser
from calendly_client import CalendlyClient
import constants as c
from helper import reset_workflow_config
from workflow import Workflow3
from workflow.notify import notify

calendly_client = None
log = None


def store_in_clipboard(clip):
    command = "printf %s | pbcopy" % clip.strip()
    os.system(command)


def main(wf):
    # type: (Workflow3) -> None

    user_input = ''.join(wf.args)

    command = user_input.split()[0]
    query = user_input[len(command) + 1:]

    log.debug("%s : %s" % (command, query))

    access_token = wf.get_password(c.ACCESS_TOKEN)

    if command == c.CMD_SINGLE_USE_LINK:
            single_use_link = calendly_client.create_link(query, 1, access_token)
            store_in_clipboard(single_use_link)
            notify("Link stored in Clipboard", "%s" % single_use_link)

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

    calendly_client = CalendlyClient(
            wf.get_password(c.CLIENT_ID),
            wf.get_password(c.CLIENT_SECRET),
            wf.settings.get(c.CONF_REDIRECT_URL, "http://localhost")
        )

    sys.exit(wf.run(main))
