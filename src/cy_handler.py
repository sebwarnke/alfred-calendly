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

    if command == c.CMD_OBTAIN_ACCESS_TOKEN:
        webbrowser.open(c.CALENDLY_API_WEB_HOOKS_URL)
        return 0;
    elif command == c.CMD_SET_ACCESS_TOKEN:
        wf.save_password(c.ACCESS_TOKEN, query)
        notify(
            "Personal Access Tolen saved to Keychain",
            "This workflow can access Calendly now. Use 'cy' command to get started.")
        return 0;

    access_token = wf.get_password(c.ACCESS_TOKEN)

    calendly_client = CalendlyClient(access_token)

    if command == c.CMD_SINGLE_USE_LINK:
        single_use_link = calendly_client.create_link(query, 1)
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

    sys.exit(wf.run(main))
