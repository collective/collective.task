# -*- coding: utf-8 -*-

from imio.helpers.catalog import addOrUpdateIndexes, addOrUpdateColumns
from imio.migrator.migrator import Migrator

import logging
logger = logging.getLogger('collective.task')


class Migrate_To_2_2(Migrator):

    def __init__(self, context):
        Migrator.__init__(self, context)

    def runProfileSteps(self, profile, steps):
        ''' Run specific steps for profile '''
        for step_id in steps:
            self.portal.portal_setup.runImportStepFromProfile('profile-%s:default' % profile, step_id)

    def run(self):
        logger.info('Migrating to collective.task 2.2')
        self.cleanRegistries()

        addOrUpdateIndexes(self.portal, indexInfos={'due_date': ('DateIndex', {})})
        addOrUpdateColumns(self.portal, columns=('due_date', ))

        self.finish()


def migrate(context):
    '''
    '''
    Migrate_To_2_2(context).run()
