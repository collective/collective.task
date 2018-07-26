# -*- coding: utf-8 -*-

from collective.task.setuphandlers import PARENTS_FIELDS_CONFIG
from imio.migrator.migrator import Migrator
from plone import api
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import logging


logger = logging.getLogger('collective.task')


class Migrate_To_100(Migrator):

    def __init__(self, context):
        Migrator.__init__(self, context)
        self.catalog = api.portal.get_tool('portal_catalog')

    def run(self):
        logger.info('Migrating to collective.task 100')
        self.cleanRegistries()
        self.runProfileSteps('collective.task', steps=['typeinfo', 'plone.app.registry', 'workflow'])
        self.portal.portal_workflow.updateRoleMappings()
        # Update existing objects
        for brain in self.catalog(portal_type='task'):
            obj = brain.getObject()
            obj.__ac_local_roles_block__ = True
            obj.parents_assigned_groups = None
            obj.parents_enquirers = None
            obj.reindexObjectSecurity()

        # settings config
        registry = getUtility(IRegistry)
        # if not registry.get('collective.task.parents_fields'):
        if True:
            registry['collective.task.parents_fields'] = PARENTS_FIELDS_CONFIG

        self.finish()


def migrate(context):
    '''
    '''
    Migrate_To_100(context).run()
