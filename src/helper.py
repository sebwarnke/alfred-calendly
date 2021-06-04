# encoding: utf-8

import constants as c


def reset_workflow_config(wf):
    try:
        wf.clear_settings()
        wf.clear_cache()
        wf.delete_password(c.CLIENT_ID)
        wf.delete_password(c.CLIENT_SECRET)
        wf.delete_password(c.REFRESH_TOKEN)
        wf.delete_password(c.ACCESS_TOKEN)
    except:
        pass
