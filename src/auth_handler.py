#!/usr/bin/python
# encoding: utf-8

import sys
import webbrowser
from workflow import Workflow3, web, notify
from calendly_client import CalendlyClient
from api_helper import reset_workflow_config
import constants as c


def build_authorization_url(client_id):
    return c.CALENDLY_AUTHORIZATION_URL_BASE \
        + "&%s=%s" % (c.CALENDLY_AUTHORIZATION_URL_PARAM_REDIRECT_URL, wf.settings.get(c.CONF_REDIRECT_URL, "http://localhost")) \
        + "&%s=%s" % (c.CALENDLY_AUTHORIZATION_URL_PARAM_CLIENT_ID, client_id)


def main(wf):
    # type: (Workflow3) -> None

    log = wf.logger

    calendly_client = CalendlyClient(
        wf.get_password(c.CLIENT_ID),
        wf.get_password(c.CLIENT_SECRET),
        wf.settings.get(c.CONF_REDIRECT_URL, "http://localhost")
    )

    user_input = ''.join(wf.args)

    command = user_input.split()[0]
    query = user_input[len(command) + 1:]

    log.debug("%s : %s" % (command, query))

    if command == c.CMD_CLIENT_CREDS:
        credentials = query.split(":")

        if len(credentials) != 2:
            print("Credentials Parameter malformed. Please try again.")
        else:
            client_id = query.split(":")[0]
            client_secret = query.split(":")[1]
            wf.save_password(c.CLIENT_ID, client_id)
            wf.save_password(c.CLIENT_SECRET, client_secret)
            print("Credentials saved for Client ID <%s>" % client_id)

    elif command == c.CMD_START_FLOW:
        client_id = wf.get_password(c.CLIENT_ID)
        webbrowser.open(build_authorization_url(client_id))

    elif command == c.CMD_REDIRECT_URI:
        wf.settings[c.CONF_REDIRECT_URL] = query
        print("Redirect URL saved in Workflow Settings.")

    elif command == c.CMD_AUTHORIZE:
        log.debug("Code: %s" % query)

        auth_result = calendly_client.authorize(query)
        if auth_result is None:
            notify(
                "Calendly Access Rejected",
                "Something went wrong. Check workflow's logs."
            )
        else:
            wf.save_password(c.ACCESS_TOKEN, auth_result.get(c.ACCESS_TOKEN))
            wf.save_password(c.REFRESH_TOKEN, auth_result.get("refresh_token"))
            notify(
                "Calendly Access Granted",
                "This workflow can access Calendly now. Use 'cy' command to get started.")

    elif command == c.CMD_RESET:
        try:
            reset_workflow_config(wf)
        finally:
            print("All local data deleted.")


if __name__ == u"__main__":
    wf = Workflow3()
    sys.exit(wf.run(main))
