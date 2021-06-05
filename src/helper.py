# encoding: utf-8

import constants as c


def reset_workflow_config(wf):
    try:
        wf.clear_settings()
        wf.clear_cache()
        wf.delete_password(c.ACCESS_TOKEN)
    except:
        pass
