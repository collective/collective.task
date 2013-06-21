from zope.interface import implements
from zope import schema
from z3c.relationfield.schema import RelationChoice

from plone.app.dexterity.behaviors.metadata import IBasic
from plone.autoform import directives as form
from plone.dexterity.content import Item
from plone.formwidget.contenttree.source import UUIDSourceBinder
from plone.formwidget.datetime.z3cform.widget import DatetimeFieldWidget
from plone.supermodel import model

from collective.z3cform.rolefield.field import LocalRolesToPrincipals

from collective.task import _


class IOpinion(model.Schema):
    """Schema for opinion"""
    title = schema.TextLine(title=_(u'Title'))
    note = schema.Text(title=_(u'Note'))
    version = RelationChoice(title=_(u"Version"),
                             source=UUIDSourceBinder(portal_type='dmsmainfile'),
                             required=False)

    deadline = schema.Datetime(title=_(u'Deadline'),
                               required=False)
    form.widget(deadline=DatetimeFieldWidget)

    addressee = LocalRolesToPrincipals(
        title=_(u"Addressee"),
        roles_to_assign=('Editor',),
        value_type=schema.Choice(
            vocabulary="plone.principalsource.Principals"
        ),
        min_length=1,
        max_length=1,
        required=True,
    )


class Opinion(Item):
    """Opinion content type"""
    implements(IOpinion)

    meta_type = 'opinion'
    # disable local roles inheritance
    __ac_local_roles_block__ = True
