from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from plone.dexterity.content import Container

from collective.task.interfaces import IBaseTask, IDeadline


class ITask(IBaseTask, IDeadline):
    """Schema for task"""
    pass


class Task(Container):
    """Task content type"""
    implements(ITask)

    enquirer = FieldProperty(ITask['enquirer'])

    responsible = FieldProperty(ITask['responsible'])

    meta_type = 'task'
    # disable local roles inheritance
    __ac_local_roles_block__ = True
