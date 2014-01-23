from zope.interface import implements

from zope.schema.fieldproperty import FieldProperty
from plone.autoform import directives as form
from plone.dexterity.content import Item
from plone.directives.form import default_value

from collective.task.interfaces import IBaseTask


class IInformation(IBaseTask):
    """Schema for information"""
    form.mode(title='hidden')


class Information(Item):
    """Information content type"""
    implements(IInformation)

    enquirer = FieldProperty(IInformation['enquirer'])

    responsible = FieldProperty(IInformation['responsible'])

    meta_type = 'information'
    # disable local roles inheritance
    __ac_local_roles_block__ = True


@default_value(field=IInformation['title'])
def titleDefaultValue(data):
    return u"Pour information"
