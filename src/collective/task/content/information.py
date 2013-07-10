from zope.interface import implements

from plone.dexterity.content import Item

from collective.task.interfaces import IBaseTask
from collective.task.catalog import SECURITY_INDEXES


class IInformation(IBaseTask):
    """Schema for information"""
    pass


class Information(Item):
    """Information content type"""
    implements(IInformation)

    meta_type = 'information'
    # disable local roles inheritance
    __ac_local_roles_block__ = True
    _cmf_security_indexes = SECURITY_INDEXES
