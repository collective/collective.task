# -*- coding: utf-8 -*-

from collective.task.interfaces import ITaskContent
from plone.dexterity.content import Container
from zope.interface import implements


class Task(Container):
    """ Task class """
    implements(ITaskContent)

    # disable local roles inheritance
    __ac_local_roles_block__ = True
