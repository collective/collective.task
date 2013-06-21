from zope.interface import implements
from zope import schema

from plone.app.dexterity.behaviors.metadata import IBasic
from plone.autoform import directives as form
from plone.dexterity.content import Item
from plone.formwidget.datetime.z3cform.widget import DatetimeFieldWidget
from plone.supermodel import model

from collective.z3cform.rolefield.field import LocalRolesToPrincipals

from collective.task import _



class IInformation(model.Schema):
    """Schema for information"""
    title = schema.TextLine(title=_(u'Title'))
    note = schema.Text(title=_(u'Note'))
    addressee = LocalRolesToPrincipals(
        title=_(u"Addressee"),
        roles_to_assign=('Reader',),
        value_type=schema.Choice(
            vocabulary="plone.principalsource.Principals"
        ),
        min_length=1,
        max_length=1,
        required=True,
    )


class Information(Item):
    """Information content type"""
    implements(IInformation)

    meta_type = 'information'
    # disable local roles inheritance
    __ac_local_roles_block__ = True
