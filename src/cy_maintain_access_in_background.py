# encoding: utf-8

from urllib2 import HTTPError
from src.workflow import Workflow3, web, PasswordNotFound
import src.constants as c
import sys

log = None


def introspect_and_conditionally_refresh_access_token():
    wf.settings["foo"] = "bar"
    # try:
    #     client_id = wf.get_password(c.CLIENT_ID)
    #     client_secret = wf.get_password(c.CLIENT_SECRET)
    #     access_token = wf.get_password(c.ACCESS_TOKEN)
    #     refresh_token = wf.get_password(c.REFRESH_TOKEN)
    #
    #     log.debug("Introspecting Access Token")
    #
    #     response = web.post(
    #         url="%s%s" % (c.CALENDLY_AUTH_BASE_URL, c.CALENDLY_INTROSPECT_URI),
    #         data={
    #             "client_id": client_id,
    #             "client_secret": client_secret,
    #             "token": access_token
    #         }
    #     )
    #     response.raise_for_status()
    #
    #     response_json = response.json()
    #     if response_json["active"] is False:
    #         log.debug("Access Token expired, Refreshing...")
    #         response = web.post(
    #             url="%s%s" % (c.CALENDLY_AUTH_BASE_URL, c.CALENDLY_TOKEN_URI),
    #             data={
    #                 "client_id": client_id,
    #                 "client_secret": client_secret,
    #                 "refresh_token": refresh_token,
    #                 "grant_type": "refresh_token"
    #             }
    #         )
    #         response.raise_for_status()
    #
    #         if response.status_code == 200:
    #             response_json = response.json()
    #             wf.save_password(c.ACCESS_TOKEN, response_json["access_token"])
    #             wf.save_password(c.REFRESH_TOKEN, response_json["refresh_token"])
    #             log.debug("Access Token refreshed.")
    #         else:
    #             log.warn("Refreshing failed. Status Code: %s" % response.status_code)
                # wf.add_item(
                #     title="Authentication API Error",
                #     subtitle="Calendly returned an error whilst checking your OAuth Access Token.",
                #     valid=False
                # )
                # wf.send_feedback()

    # except PasswordNotFound:
    #     wf.add_item(
    #         title="No Calendly Client registered yet.",
    #         subtitle="Use 'cya' to start authentication flow.",
    #         valid=False
    #     )
    #     wf.send_feedback()
    #
    # except HTTPError:
    #     wf.add_item(
    #         title="Authentication API Error",
    #         subtitle="Calendly returned an error whilst checking your OAuth Access Token.",
    #         valid=False
    #     )
    #     wf.send_feedback()


def main(wf):
    # type: (Workflow3) -> None
    introspect_and_conditionally_refresh_access_token()


if __name__ == '__main__':
    wf = Workflow3()
    log = wf.logger
    log.debug("I am alive")
    log.debug(wf)
    sys.exit(wf.run(main))
