# -*- coding: utf-8 -*-

from imio.helpers.catalog import addOrUpdateColumns
from imio.helpers.catalog import addOrUpdateIndexes
from imio.migrator.migrator import Migrator

import logging


logger = logging.getLogger("collective.task")


class Migrate_To_2_2(Migrator):
    def __init__(self, context):
        Migrator.__init__(self, context)

    def run(self):
        logger.info("Migrating to collective.task 2.2")
        self.cleanRegistries()

        addOrUpdateIndexes(
            self.portal, indexInfos={"assigned_group": ("FieldIndex", {}), "due_date": ("DateIndex", {})}
        )
        addOrUpdateColumns(self.portal, columns=("assigned_group", "due_date"))

        self.runProfileSteps("collective.task", steps=["typeinfo", "workflow", "cssregistry"])
        self.finish()


def migrate(context):
    """ """
    Migrate_To_2_2(context).run()
