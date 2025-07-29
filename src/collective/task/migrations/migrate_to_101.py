# -*- coding: utf-8 -*-

from imio.migrator.migrator import Migrator
from plone import api

import logging


logger = logging.getLogger("collective.task")


class Migrate_To_101(Migrator):
    def __init__(self, context):
        Migrator.__init__(self, context)
        self.catalog = api.portal.get_tool("portal_catalog")

    def run(self):
        logger.info("Migrating to collective.task 101")
        self.cleanRegistries()
        setup = api.portal.get_tool("portal_setup")
        ir = setup.getImportStepRegistry()
        if "task-uninstall" in ir._registered:
            del ir._registered["task-uninstall"]
            setup._p_changed = True
        self.finish()


def migrate(context):
    """ """
    Migrate_To_101(context).run()
