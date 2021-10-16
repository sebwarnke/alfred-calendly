# encoding: utf-8

from workflow import Workflow3
from workflow.update import Version


def process_migration(wf):
    # type: (Workflow3) -> None

    if wf.first_run:
        last_version = wf.last_version_run
        current_version = wf.version

        if current_version is not None and last_version is not None:

            wf.logger.debug("This is the first run after update; %s -> %s" % (last_version, current_version))

            if last_version < Version("2.0.0") <= current_version:
                migrate_1_x_x_to_2_x_x(wf)


def migrate_1_x_x_to_2_x_x(wf):
    wf.logger.debug("Migrating 1.X.X -> 2.X.X")
    try:
        wf.clear_settings()
        wf.clear_cache()
        wf.delete_password("calendly_alfred_client_id")
        wf.delete_password("calendly_alfred_client_secret")
        wf.delete_password("calendly_alfred_access_token")
        wf.delete_password("calendly_alfred_refresh_token")
    except:
        pass
