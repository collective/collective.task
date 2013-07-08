from zope.interface import implements

from plone.dexterity.content import Item

from collective.task.interfaces import BaseTask
from collective.task.interfaces import IBaseTask


class IValidation(IBaseTask):
    """Schema for validation"""
    pass


class Validation(BaseTask, Item):
    """Validation content type"""
    implements(IValidation)

    meta_type = 'validation'
    # disable local roles inheritance
    __ac_local_roles_block__ = True
