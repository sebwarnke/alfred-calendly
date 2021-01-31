#!/usr/bin/python
# encoding: utf-8

import sys
import webbrowser
from workflow import Workflow3, web
from urllib2 import HTTPError

import constants as c

log = None


def build_authorization_url(client_id):
    return c.CALENDLY_AUTHORIZATION_URL_BASE \
        + "&%s=%s" % (c.CALENDLY_AUTHORIZATION_URL_PARAM_REDIRECT_URL, wf.settings.get(c.CONF_REDIRECT_URL, "http://localhost")) \
        + "&%s=%s" % (c.CALENDLY_AUTHORIZATION_URL_PARAM_CLIENT_ID, client_id)


def main(wf):
    # type: (Workflow3) -> None

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
        client_id = wf.get_password(c.CLIENT_ID)
        client_secret = wf.get_password(c.CLIENT_SECRET)

        response = web.post(
            url="%s%s" % (c.CALENDLY_AUTH_BASE_URL, c.CALENDLY_TOKEN_URI),
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
            wf.save_password(c.ACCESS_TOKEN, json["access_token"])
            wf.save_password(c.REFRESH_TOKEN, json["refresh_token"])
            print("Calendly Access granted.")


if __name__ == u"__main__":
    wf = Workflow3()
    log = wf.logger

    sys.exit(wf.run(main))
