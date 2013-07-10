from zope.interface import implements

from plone.dexterity.content import Item

from collective.task.interfaces import IBaseTask
from collective.task.catalog import SECURITY_INDEXES


class IOpinion(IBaseTask):
    """Schema for opinion"""
    pass


class Opinion(Item):
    """Opinion content type"""
    implements(IOpinion)

    meta_type = 'opinion'
    # disable local roles inheritance
    __ac_local_roles_block__ = True
    _cmf_security_indexes = SECURITY_INDEXES
