#!/usr/bin/python
# encoding: utf-8

import sys

from workflow import Workflow3, PasswordNotFound
import constants as c

log = None


def main(wf):
    # type: (Workflow3) -> None

    user_input = wf.args[0]
    command = query = ""
    if len(user_input) > 0:
        command = user_input.split()[0]
        query = user_input[len(command) + 1:]

    client_is_registered = True
    try:
        wf.get_password(c.CLIENT_ID)
        wf.get_password(c.CLIENT_SECRET)
    except PasswordNotFound:
        client_is_registered = False

    auth_code_exists = True
    try:
        wf.get_password(c.ACCESS_TOKEN)
        wf.get_password(c.REFRESH_TOKEN)
    except PasswordNotFound:
        auth_code_exists = False

    if client_is_registered is False:
        if command == "":
            wf.add_item(
                title="No Calendly Client registered yet",
                subtitle="Hit ENTER to proceed with registration.",
                autocomplete="%s " % c.CMD_CLIENT_CREDS,
                valid=False
            )
        elif command == c.CMD_CLIENT_CREDS:
            if query == '':
                wf.add_item(
                    title="Add Calendly OAuth Client Credentials and hit ENTER",
                    subtitle="Use Syntax: '<CLIENT_ID>:<CLIENT_SECRET>'",
                    valid=False
                )
            else:
                wf.add_item(
                    title="Add Calendly OAuth Client Credentials and hit ENTER",
                    subtitle="Use Syntax: '<CLIENT_ID>:<CLIENT_SECRET>'",
                    arg="%s %s" % (c.CMD_CLIENT_CREDS, query),
                    valid=True
                )
    elif auth_code_exists is False:
        if command == "":
            wf.add_item(
                title="No Refresh Token and no Auth Code found",
                subtitle="Hit ENTER to proceed.",
                autocomplete="%s " % c.CMD_AUTHORIZE,
                valid=False
            )
        elif command == c.CMD_AUTHORIZE:
            if query == '':
                wf.add_item(
                    title="Paste your Authorization Code here.",
                    subtitle="If you don't have one, simply press ENTER.",
                    arg=c.CMD_START_FLOW,
                    valid=True
                )
            else:
                wf.add_item(
                    title="Add Calendly OAuth Client Credentials and hit ENTER",
                    subtitle="Use Syntax: '<CLIENT_ID>:<CLIENT_SECRET>'",
                    arg="%s %s" % (c.CMD_AUTHORIZE, query),
                    valid=True
                )

    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main))
