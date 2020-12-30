#!/usr/bin/python
# encoding: utf-8

import sys
import webbrowser
from workflow import Workflow3

from constants import __cmd_client_creds__, __client_id__, __client_secret__, __authorization_url__, __cmd_start_flow__

log = None


def main(wf):
    # type: (Workflow3) -> None

    user_input = ''.join(wf.args)

    command = user_input.split()[0]
    query = user_input[len(command) + 1:]

    log.debug("%s : %s" % (command, query))

    if command == __cmd_client_creds__:
        credentials = query.split(":")

        if len(credentials) != 2:
            print("Credentials Parameter malformed. Please try again.")
        else:
            client_id = query.split(":")[0]
            client_secret = query.split(":")[1]
            wf.save_password(__client_id__, client_id)
            wf.save_password(__client_secret__, client_secret)
            print("Credentials saved for Client ID <%s>" % client_id)
    elif command == __cmd_start_flow__:
        client_id = wf.get_password(__client_id__)
        webbrowser.open(__authorization_url__ + client_id)


if __name__ == u"__main__":
    wf = Workflow3()
    log = wf.logger

    sys.exit(wf.run(main))
