# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from collective.task import _
from collective.z3cform.datagridfield.registry import DictRow
from dexterity.localrolesfield.field import LocalRolesField
from plone.app.dexterity import PloneMessageFactory as _PMF
from plone.autoform import directives
from plone.supermodel import model
from z3c.form.browser.select import SelectFieldWidget
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class ICollectiveTaskLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class ITaskContent(model.Schema):
    """ Interface for task content type """

    title = schema.TextLine(
        title=_PMF(u'label_title', default=u'Title'),
        required=True
    )

    parents_assigned_groups = LocalRolesField(
        title=_(u"Parents assigned groups"),
        required=False,
        value_type=schema.Choice(vocabulary=u'collective.task.AssignedGroups')
    )
    # must change widget to hide it, because default widget (orderedselect) doesn't have hidden widget template
    directives.widget('parents_assigned_groups', SelectFieldWidget, multiple='multiple', size=10)
    directives.mode(parents_assigned_groups='hidden')

    parents_enquirers = LocalRolesField(
        title=_(u"Parents enquirers"),
        required=False,
        value_type=schema.Choice(vocabulary=u'collective.task.Enquirer')
    )
    # must change widget to hide it, because default widget (orderedselect) doesn't have hidden widget template
    directives.widget('parents_enquirers', SelectFieldWidget, multiple='multiple', size=10)
    directives.mode(parents_enquirers='hidden')


class ITaskMethods(Interface):

    def get_highest_task_parent(task=False):
        """
            Get the object containing the highest ITask object
            or the highest ITask object if task is True
        """


class ITaskContainerMethods(Interface):
    """ Adapter description """


class ITaskContentMethods(Interface):
    """ Adapter description """


class IParentsFieldSchema(Interface):
    fieldname = schema.TextLine(title=_("Parents field name"), required=True)
    attribute = schema.TextLine(title=_("Parent attribute"), required=True)
    attribute_prefix = schema.TextLine(title=_("Attribute prefix (without dot)"), required=False)
    provided_interface = schema.TextLine(title=_("Parent interface"), required=True)


class ICollectiveTaskConfig(model.Schema):

    parents_fields = schema.List(
        title=_(u'Parents fields'),
        value_type=DictRow(title=_("Parents field"),
                           schema=IParentsFieldSchema))
