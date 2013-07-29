from zope.interface import implements

from plone.dexterity.content import Item

from collective.task.interfaces import IBaseTask, IDeadline


class IOpinion(IBaseTask, IDeadline):
    """Schema for opinion"""
    pass


class Opinion(Item):
    """Opinion content type"""
    implements(IOpinion)

    meta_type = 'opinion'
    # disable local roles inheritance
    __ac_local_roles_block__ = True
