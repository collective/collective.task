from zope.interface import implements

from plone.dexterity.content import Item

from collective.task.interfaces import BaseTask
from collective.task.interfaces import IBaseTask


class IInformation(IBaseTask):
    """Schema for information"""
    pass


class Information(BaseTask, Item):
    """Information content type"""
    implements(IInformation)

    meta_type = 'information'
    # disable local roles inheritance
    __ac_local_roles_block__ = True
