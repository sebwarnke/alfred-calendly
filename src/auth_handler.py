#!/usr/bin/python
# encoding: utf-8

import sys
import webbrowser

import constants as c
from helper import reset_workflow_config
from calendly_client import CalendlyClient
from workflow import Workflow3
from workflow.notify import notify


def main(wf):
    # type: (Workflow3) -> None

    log = wf.logger

    user_input = ''.join(wf.args)

    command = user_input.split()[0]
    query = user_input[len(command) + 1:]

    if command == c.CMD_OBTAIN_ACCESS_TOKEN:
        webbrowser.open(c.CALENDLY_API_WEB_HOOKS_URL)

    elif command == c.CMD_SET_ACCESS_TOKEN:
        wf.save_password(c.ACCESS_TOKEN, query)
        notify(
            "Personal Access Tolen saved to Keychain",
            "This workflow can access Calendly now. Use 'cy' command to get started.")

    elif command == c.CMD_RESET:
        try:
            reset_workflow_config(wf)
        finally:
            notify("Authentication Reset", "All local data deleted.")


if __name__ == u"__main__":
    wf = Workflow3()
    sys.exit(wf.run(main))
