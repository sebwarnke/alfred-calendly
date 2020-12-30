#!/usr/bin/python
# encoding: utf-8

import sys

from workflow import Workflow3, PasswordNotFound
from constants \
    import __client_id__, __client_secret__, __cmd_client_creds__, __auth_code__, __cmd_authorize__, \
    __authorization_url__, __cmd_start_flow__

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
        wf.get_password(__client_id__)
        wf.get_password(__client_secret__)
    except PasswordNotFound:
        client_is_registered = False

    auth_code_exists = True
    try:
        wf.get_password(__auth_code__)
    except PasswordNotFound:
        auth_code_exists = False

    if client_is_registered is False:
        if command == "":
            wf.add_item(
                title="No Calendly Client registered yet",
                subtitle="Hit ENTER to proceed with registration.",
                autocomplete="%s " % __cmd_client_creds__,
                valid=False
            )
        elif command == __cmd_client_creds__:
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
                    arg="%s %s" % (__cmd_client_creds__, query),
                    valid=True
                )
    elif auth_code_exists is False:
        if command == "":
            wf.add_item(
                title="No Refresh Token and no Auth Code found",
                subtitle="Hit ENTER to proceed.",
                autocomplete="%s " % __cmd_authorize__,
                valid=False
            )
        elif command == __cmd_authorize__:
            if query == '':
                wf.add_item(
                    title="Paste your Authorization Code here.",
                    subtitle="If you don't have one, simply press ENTER.",
                    arg=__cmd_start_flow__,
                    valid=True
                )
            else:
                wf.add_item(
                    title="Add Calendly OAuth Client Credentials and hit ENTER",
                    subtitle="Use Syntax: '<CLIENT_ID>:<CLIENT_SECRET>'",
                    arg="%s %s" % (__cmd_authorize__, __authorization_url__),
                    valid=True
                )

    wf.send_feedback()

    # if args.query is not None:
    #     log.debug("query=" + args.query)
    #
    # if args.client_id:
    #     wf.save_password(__client_id__, args.client_id)
    #
    # if args.client_secret:
    #     wf.save_password(__client_secret__, args.client_secret)
    #
    # if args.auth_code:
    #     wf.save_password(__auth_code__, args.auth_code)
    #
    # try:
    #     wf.get_password(__client_id__)
    # except PasswordNotFound:
    #     wf.add_item(
    #         title="Set Client ID",
    #         subtitle="The Client ID received from Calendly Client Registration",
    #         autocomplete="client_id ",
    #         valid=False
    #     )
    #
    # try:
    #     wf.get_password(__client_secret__)
    # except PasswordNotFound:
    #     wf.add_item(title="Set Client Secret")
    #
    # try:
    #     wf.get_password(__auth_code__)
    # except PasswordNotFound:
    #     wf.add_item(title="Authorization Code")
    #
    # wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main))
