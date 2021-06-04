#!/usr/bin/python
# encoding: utf-8

import sys

from workflow import Workflow3, PasswordNotFound, ICON_EJECT
import constants as c
from migration import process_migration

log = None


def main(wf):
    # type: (Workflow3) -> None

    user_input = wf.args[0]
    command = query = ""
    if len(user_input) > 0:
        command = user_input.split()[0]
        query = user_input[len(command) + 1:]

    access_token_exists = True
    try:
        wf.get_password(c.ACCESS_TOKEN)
    except PasswordNotFound:
        access_token_exists = False

    if command == c.CMD_RESET:
        wf.add_item(
            title="Reset Authentication",
            subtitle="This remove all local data. ARE YOU SURE?",
            arg="%s" % c.CMD_RESET,
            valid=True,
            icon=ICON_EJECT
        )
        wf.send_feedback()
        return 0

    if access_token_exists is False:
        if command == "":
            wf.add_item(
                title="Please set your Personal Access Token.",
                subtitle="Hit ENTER to proceed.",
                autocomplete="%s " % c.CMD_SET_ACCESS_TOKEN,
                valid=False
            )
        elif command == c.CMD_SET_ACCESS_TOKEN:
            if query == '':
                wf.add_item(
                    title="Paste your Personal Access Token here.",
                    subtitle="If you don't have one, simply press ENTER.",
                    arg=c.CMD_OBTAIN_ACCESS_TOKEN,
                    valid=True
                )
            else:
                wf.add_item(
                    title="Hit ENTER to save your Personal Access Token.",
                    subtitle="You can now enter the command 'cy' to use this workflow.",
                    arg="%s %s" % (c.CMD_SET_ACCESS_TOKEN, query),
                    valid=True
                )

    wf.add_item(
        title="Reset Authentication",
        subtitle="This removes all local data.",
        autocomplete="%s" % c.CMD_RESET,
        valid=False,
        icon=ICON_EJECT
    )

    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow3()
    log = wf.logger

    process_migration(wf)

    sys.exit(wf.run(main))
