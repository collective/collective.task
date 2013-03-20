from zope.interface import implements
from zope import schema

from plone.dexterity.content import Container
from plone.supermodel import model

from collective.task import _


class ITask(model.Schema):
    title = schema.TextLine(title=_(u'Title'))
    deadline = schema.Date(title=_(u'Date'), required=False)


class Task(Container):
    implements(ITask)
