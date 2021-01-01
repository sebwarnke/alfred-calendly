#!/usr/bin/python
# encoding: utf-8

import sys
import webbrowser
from workflow import Workflow3, web
from urllib2 import HTTPError

from constants import __cmd_client_creds__, __client_id__, __client_secret__, __authorization_url__, __cmd_start_flow__, \
    __cmd_authorize__, __token_url__, __refresh_token__, __access_token__

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

    elif command == __cmd_authorize__:
        client_id = wf.get_password(__client_id__)
        client_secret = wf.get_password(__client_secret__)

        response = web.post(
            url=__token_url__,
            data={
                "grant_type": "authorization_code",
                "client_id": client_id,
                "client_secret": client_secret,
                "code": query,
                "redirect_uri": "https://www.calendly.sebwarnke.com"
            }
        )

        log.debug("ID: %s" % client_id)
        log.debug("Secret: %s" % client_secret)
        log.debug("Code: %s" % query)

        try:
            response.raise_for_status()
        except HTTPError as e:
            error_msg = "HTTP Request Failed: %d" % response.status_code
            log.error(error_msg)
            log.debug("%d - %s" % (e.code, e.reason))
            print(error_msg)
            return 0

        if response.status_code == 200:
            json = response.json()
            log.debug(json)
            wf.save_password(__access_token__, json["access_token"])
            wf.save_password(__refresh_token__, json["refresh_token"])
            print("Calendly Access granted.")


if __name__ == u"__main__":
    wf = Workflow3()
    log = wf.logger

    sys.exit(wf.run(main))
