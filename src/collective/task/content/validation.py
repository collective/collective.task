from zope.interface import implements

from plone.dexterity.content import Item

from collective.task.interfaces import IBaseTask, IDeadline


class IValidation(IBaseTask, IDeadline):
    """Schema for validation"""
    pass


class Validation(Item):
    """Validation content type"""
    implements(IValidation)

    meta_type = 'validation'
    # disable local roles inheritance
    __ac_local_roles_block__ = True
