from z3c.relationfield.schema import RelationChoice
from zope.interface import alsoProvides

from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.formwidget.contenttree.source import ObjPathSourceBinder
from plone.supermodel import model

from collective.task import _


class ITarget(model.Schema):
    """Target behavior"""
    target = RelationChoice(title=_(u"Target"),
                            source=ObjPathSourceBinder(),
                            required=False)
    form.mode(target="hidden")


alsoProvides(ITarget, IFormFieldProvider)
