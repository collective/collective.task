from zope.interface import implements

from plone.dexterity.content import Item

from collective.task.interfaces import IBaseTask
from collective.task.catalog import SECURITY_INDEXES


class IValidation(IBaseTask):
    """Schema for validation"""
    pass


class Validation(Item):
    """Validation content type"""
    implements(IValidation)

    meta_type = 'validation'
    # disable local roles inheritance
    __ac_local_roles_block__ = True
    _cmf_security_indexes = SECURITY_INDEXES
