# encoding: utf-8

import sys
from workflow import Workflow3
from api_helper import get_event_types_for_current_user
import constants as c

log = None


def main(wf):
    # type: (Workflow3) -> None
    log.debug("Loading Event Types for current user.")
    wf.cache_data(c.CACHE_EVENT_TYPES, get_event_types_for_current_user())


if __name__ == '__main__':
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main))
