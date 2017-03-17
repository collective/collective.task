# -*- coding: utf-8 -*-

from zope.interface import implements
from plone.dexterity.content import Container
from collective.task.interfaces import ITaskContent


class Task(Container):
    """ Task class """
    implements(ITaskContent)

    # disable local roles inheritance
    __ac_local_roles_block__ = True
