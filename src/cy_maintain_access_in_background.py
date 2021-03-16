# encoding: utf-8

from urllib2 import HTTPError
from workflow import Workflow3, notify, PasswordNotFound
import constants as c
from calendly_client import CalendlyClient
import sys

log = None
calendly_client = None


def introspect_and_conditionally_refresh_access_token():
    try:
        log.debug("Introspecting Access Token")
        access_token = wf.get_password(c.ACCESS_TOKEN)
        refresh_token = wf.get_password(c.REFRESH_TOKEN)

        is_active = calendly_client.introspect(access_token)

        if is_active:
            log.debug("Access Token still valid. No action required.")
        else:
            log.debug("Access Token expired, Refreshing...")

            result = calendly_client.refresh_token(refresh_token)

            if result is not None:
                wf.save_password(c.ACCESS_TOKEN, result.get(c.ACCESS_TOKEN))
                wf.save_password(c.REFRESH_TOKEN, result.get(c.REFRESH_TOKEN))
            else:
                notify("Authentication Error", "Authentication could not be refreseh. Please, check the log.")

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

    calendly_client = CalendlyClient(
        wf.get_password(c.CLIENT_ID),
        wf.get_password(c.CLIENT_SECRET),
        wf.settings.get(c.CONF_REDIRECT_URL, "http://localhost")
    )

    sys.exit(wf.run(main))
