# encoding: utf-8

import sys
from workflow import Workflow3
from calendly_client import CalendlyClient
import constants as c

log = None


def main(wf):
    # type: (Workflow3) -> None
    log.debug("Loading Event Types for current user.")

    access_token = wf.get_password(c.ACCESS_TOKEN)

    calendly_client = CalendlyClient(
            wf.get_password(c.CLIENT_ID),
            wf.get_password(c.CLIENT_SECRET),
            wf.settings.get(c.CONF_REDIRECT_URL, "http://localhost")
        )

    current_user = calendly_client.get_current_user(access_token)

    if current_user is not None:
        event_types = calendly_client.get_event_types_of_user(current_user,access_token)
        if event_types is not None:
            wf.cache_data(c.CACHE_EVENT_TYPES, event_types)
        else:
            raise Exception("Failed loading Event Types. API request failed. See log.")
    else:
        raise Exception("Failed loading Event Types. Could not determine current user.")


if __name__ == '__main__':
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main))
