#!/usr/bin/python
# encoding: utf-8

import sys
from argparse import ArgumentParser
# Workflow3 supports Alfred 3's new features. The `Workflow` class
# is also compatible with Alfred 2.
from workflow import Workflow3, web


def main(wf):

    parser = ArgumentParser()
    args = parser.parse_args(wf.args)

    url = "https://api.calendly.com/event_types"
    headers = {
        "Authorization": "",
        "content-type": "application/json"
    }

    params = {
        'user': ''
    }

    response = web.get(url, headers=headers, params=params)

    # print("Response Code: " + str(response.status_code))
    event_types = []
    if response.status_code == 200:
        event_types = response.json()['collection']

    for event_type in event_types:
        # print(event_type)
        wf.add_item(
            title=event_type["name"],
            subtitle=event_type["scheduling_url"],
            arg=event_type["scheduling_url"],
            valid=True)

    # Send output to Alfred. You can only call this once.
    # Well, you *can* call it multiple times, but subsequent calls
    # are ignored (otherwise the JSON sent to Alfred would be invalid).
    wf.send_feedback()


if __name__ == '__main__':
    # Create a global `Workflow3` object
    wf = Workflow3()
    # Call your entry function via `Workflow3.run()` to enable its
    # helper functions, like exception catching, ARGV normalization,
    # magic arguments etc.
    sys.exit(wf.run(main))
