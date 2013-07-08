from zope.interface import implements

from plone.dexterity.content import Container

from collective.task.interfaces import BaseTask
from collective.task.interfaces import IBaseTask
from collective.task import _


class ITask(IBaseTask):
    """Schema for task"""
    pass


class Task(BaseTask, Container):
    """Task content type"""
    implements(ITask)

    meta_type = 'task'
    # disable local roles inheritance
    __ac_local_roles_block__ = True
