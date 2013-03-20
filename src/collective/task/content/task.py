from zope.interface import implements
from zope import schema

from plone.dexterity.content import Container
from plone.supermodel import model

from collective.dms.basecontent._field import LocalRolesToPrincipals

from collective.task import _


class ITask(model.Schema):
    title = schema.TextLine(title=_(u'Title'))
    deadline = schema.Date(title=_(u'Date'),
                           required=False)

    responsible = LocalRolesToPrincipals(
        title=_(u"Responsible"),
        roles_to_assign=('Editor',),
        required=False,
        value_type=schema.Choice(
            vocabulary="plone.principalsource.Principals"
        ),
    )


class Task(Container):
    implements(ITask)
