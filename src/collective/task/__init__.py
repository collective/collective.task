# -*- coding: utf-8 -*-
"""Init and utils."""

from zope.i18nmessageid import MessageFactory

_ = MessageFactory('collective.task')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    from .catalog import UsersAndGroupsIndex, manage_addUsersAndGroupsIndex, manage_addUsersAndGroupsIndexForm
    context.registerClass(UsersAndGroupsIndex,
                      permission='Add Pluggable Index',
                      constructors=(manage_addUsersAndGroupsIndexForm,
                                    manage_addUsersAndGroupsIndex),
                      #icon='www/index.gif',
                      visibility=None,
                     )
