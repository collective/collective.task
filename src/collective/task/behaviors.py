from zope.interface import alsoProvides
from z3c.relationfield.schema import RelationChoice

from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.formwidget.contenttree.source import UUIDSourceBinder
from plone.supermodel import model

from collective.task import _


class IRelatedVersion(model.Schema):
    """RelatedVersion behavior"""
    version = RelationChoice(title=_(u"Version"),
                             source=UUIDSourceBinder(portal_type='dmsmainfile'),
                             required=False)
    form.mode(version="hidden")


alsoProvides(IRelatedVersion, IFormFieldProvider)
