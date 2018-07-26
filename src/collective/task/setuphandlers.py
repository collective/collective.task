# -*- coding: utf-8 -*-
"""Initial setup."""
from dexterity.localroles.utils import add_fti_configuration
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import logging


logger = logging.getLogger('collective.task: setuphandlers')


PARENTS_FIELDS_CONFIG = [
    {'fieldname': u'parents_assigned_groups', 'attribute': u'assigned_group', 'attribute_prefix': u'ITask',
     'provided_interface': u'collective.task.interfaces.ITaskContent'},
    {'fieldname': u'parents_enquirers', 'attribute': u'enquirer', 'attribute_prefix': u'ITask',
     'provided_interface': u'collective.task.interfaces.ITaskContent'},
]


def isNotCurrentProfile(context):
    return context.readDataFile('collectivetask_marker.txt') is None


def configure_rolefields(context):
    """Configure the rolefields on types."""
    roles_config = {
        'static_config': {},
        'assigned_group': {
            'created': {
                '': {'roles': ['Contributor', 'Editor', 'Reviewer']}
            },
            'to_assign': {
                '': {'roles': ['Contributor', 'Editor', 'Reviewer']},
            },
            'to_do': {
                '': {'roles': ['Contributor', 'Editor', 'Reviewer']},
            },
            'in_progress': {
                '': {'roles': ['Contributor', 'Editor', 'Reviewer']},
            },
            'realized': {
                '': {'roles': ['Contributor', 'Editor', 'Reviewer']},
            },
            'closed': {
                '': {'roles': ['Contributor', 'Editor', 'Reviewer']},
            },
        },
        'assigned_user': {
            'created': {
                '': {'roles': []}
            },
            'to_assign': {
                '': {'roles': []},
            },
            'to_do': {
                '': {'roles': ['Contributor', 'Editor', 'Reviewer']},
            },
            'in_progress': {
                '': {'roles': ['Contributor', 'Editor', 'Reviewer']},
            },
            'realized': {
                '': {'roles': ['Contributor', 'Editor', 'Reviewer']},
            },
            'closed': {
                '': {'roles': []},
            },
        },
    }

    for keyname in roles_config:
        # don't overwrite existing configuration
        msg = add_fti_configuration(
            'task',
            roles_config[keyname],
            keyname=keyname)

        if msg:
            logger.warn(msg)


def post_install(context):
    """Post install script."""
    if isNotCurrentProfile(context):
        return

    logger.info('Configure role fields')
    configure_rolefields(context)

    registry = getUtility(IRegistry)
    logger.info("Configure registry")
    if not registry.get('collective.task.parents_fields'):
        registry['collective.task.parents_fields'] = PARENTS_FIELDS_CONFIG


def uninstall_1(context):
    """Uninstall script for 1.0 version."""
    if context.readDataFile('collectivetask_uninstall_1_marker.txt') is None:
        return

    site = context.getSite()
    pt = site.portal_types
    for typ in ('information', 'opinion', 'task', 'validation'):
        if typ in pt:
            pt.manage_delObjects(ids=[typ])
            logger.info("Removed %s from portal_types" % typ)

    pw = site.portal_workflow
    for wf in ('basic_task_workflow', 'task_workflow', 'validation_workflow'):
        if wf in pw:
            pw.manage_delObjects(ids=[wf])
            logger.info("Removed %s from portal_workflow" % wf)
