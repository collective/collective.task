from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from plone.dexterity.content import Item

from collective.task.interfaces import IBaseTask, IDeadline


class IOpinion(IBaseTask, IDeadline):
    """Schema for opinion"""
    pass


class Opinion(Item):
    """Opinion content type"""
    implements(IOpinion)

    enquirer = FieldProperty(IOpinion['enquirer'])

    responsible = FieldProperty(IOpinion['responsible'])

    meta_type = 'opinion'
    # disable local roles inheritance
    __ac_local_roles_block__ = True
