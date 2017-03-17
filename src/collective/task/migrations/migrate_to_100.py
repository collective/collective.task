# -*- coding: utf-8 -*-

from plone import api
from imio.migrator.migrator import Migrator

import logging
logger = logging.getLogger('collective.task')


class Migrate_To_100(Migrator):

    def __init__(self, context):
        Migrator.__init__(self, context)
        self.catalog = api.portal.get_tool('portal_catalog')

    def run(self):
        logger.info('Migrating to collective.task 100')
        self.cleanRegistries()
        self.runProfileSteps('collective.task', steps=['typeinfo'])
        # Update existing objects
        for brain in self.catalog(portal_type='task'):
            obj = brain.getObject()
            obj.__ac_local_roles_block__ = True
            obj.reindexObjectSecurity()

        self.finish()


def migrate(context):
    '''
    '''
    Migrate_To_100(context).run()
