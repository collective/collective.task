from zope.interface import implements

from plone.dexterity.content import Container

from collective.task.interfaces import IBaseTask
from collective.task.catalog import SECURITY_INDEXES


class ITask(IBaseTask):
    """Schema for task"""
    pass


class Task(Container):
    """Task content type"""
    implements(ITask)

    meta_type = 'task'
    # disable local roles inheritance
    __ac_local_roles_block__ = True
    _cmf_security_indexes = SECURITY_INDEXES
