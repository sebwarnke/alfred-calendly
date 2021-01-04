# encoding: utf-8

from urllib2 import HTTPError
from workflow import Workflow3, web, PasswordNotFound
import constants as c
import sys

log = None


def introspect_and_conditionally_refresh_access_token():
    try:
        log.debug("Introspecting Access Token")
        client_id = wf.get_password(c.CLIENT_ID)
        client_secret = wf.get_password(c.CLIENT_SECRET)
        access_token = wf.get_password(c.ACCESS_TOKEN)
        refresh_token = wf.get_password(c.REFRESH_TOKEN)

        response = web.post(
            url="%s%s" % (c.CALENDLY_AUTH_BASE_URL, c.CALENDLY_INTROSPECT_URI),
            data={
                "client_id": client_id,
                "client_secret": client_secret,
                "token": access_token
            }
        )
        response.raise_for_status()

        response_json = response.json()

        if response_json["active"] is True:
            log.debug("Access Token still valid. No action required.")
        else:
            log.debug("Access Token expired, Refreshing...")
            response = web.post(
                url="%s%s" % (c.CALENDLY_AUTH_BASE_URL, c.CALENDLY_TOKEN_URI),
                data={
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "refresh_token": refresh_token,
                    "grant_type": "refresh_token"
                }
            )
            response.raise_for_status()

            if response.status_code == 200:
                response_json = response.json()
                wf.save_password(c.ACCESS_TOKEN, response_json["access_token"])
                wf.save_password(c.REFRESH_TOKEN, response_json["refresh_token"])
                log.debug("Access Token refreshed.")
            else:
                log.warn("Refreshing failed. Status Code: %s" % response.status_code)

    except PasswordNotFound:
        log.error("Passwords not found in keychain.")

    except HTTPError as e:
        log.error("HTTP Error from Calendly: %s - %s" % (e.code, e.message))


def main(wf):
    # type: (Workflow3) -> None
    introspect_and_conditionally_refresh_access_token()


if __name__ == '__main__':
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main))
