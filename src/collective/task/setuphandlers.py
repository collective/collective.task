# -*- coding: utf-8 -*-
"""Initial setup."""
import logging

from dexterity.localroles.utils import add_fti_configuration


logger = logging.getLogger('collective.task: setuphandlers')


def isNotCurrentProfile(context):
    return context.readDataFile('collectivetask_marker.txt') is None


def configure_rolefields(context):
    """Configure the rolefields on types."""
    roles_config = {
        'localroleconfig': {},
        'assigned_group': {
            'created': {
                '': ['Contributor', 'Editor', 'Reviewer']
            },
            'to_assign': {
                '': ['Contributor', 'Editor', 'Reviewer'],
            },
            'to_do': {
                '': ['Contributor', 'Editor', 'Reviewer'],
            },
            'in_progress': {
                '': ['Contributor', 'Editor', 'Reviewer'],
            },
            'realized': {
                '': ['Contributor', 'Editor', 'Reviewer'],
            },
            'closed': {
                '': ['Contributor', 'Editor', 'Reviewer'],
            },
        },
        'assigned_user': {
            'created': {
                '': []
            },
            'to_assign': {
                '': [],
            },
            'to_do': {
                '': ['Contributor', 'Editor', 'Reviewer'],
            },
            'in_progress': {
                '': ['Contributor', 'Editor', 'Reviewer'],
            },
            'realized': {
                '': ['Contributor', 'Editor', 'Reviewer'],
            },
            'closed': {
                '': [],
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

    # Do something during the installation of this package
    configure_rolefields(context)
