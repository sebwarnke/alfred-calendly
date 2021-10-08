# encoding: utf-8

import sys
from workflow import Workflow3
from calendly_client import CalendlyClient
from calendly_client import active_filter as ACTIVE_FILTER
from controller import Controller
import constants as c

log = None

'''
This file is started as background thread. An takes care of loading event types into the cache asynchronously.
'''

def main(wf):
    # type: (Workflow3) -> None
    log.debug("Loading Event Types for current user.")
    controller = Controller(wf)
    controller.cache_ordered_event_types()


if __name__ == '__main__':
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main))
