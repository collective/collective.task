# -*- coding: utf-8 -*-
from collective.task.interfaces import ITaskContent
from collective.task.interfaces import ITaskContentMethods
from plone.dexterity.content import Container
from zope.interface import implementer


@implementer(ITaskContent)
class Task(Container):
    """Task class"""

    # disable local roles inheritance
    __ac_local_roles_block__ = True

    def get_methods_adapter(self):
        """Returns the adapter providing methods"""
        return ITaskContentMethods(self)
