# -*- coding: utf-8 -*-

from imio.migrator.migrator import Migrator

import logging


logger = logging.getLogger('collective.task')


class Migrate_To_2_2_2(Migrator):

    def __init__(self, context):
        Migrator.__init__(self, context)

    def run(self):
        logger.info('Migrating to collective.task 2.2.2')
        self.cleanRegistries()

        self.runProfileSteps('collective.task', steps=['workflow'])
        self.finish()


def migrate(context):
    '''
    '''
    Migrate_To_2_2_2(context).run()
