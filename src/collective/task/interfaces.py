# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from plone.app.dexterity import PloneMessageFactory as _PMF
from plone.supermodel import model


class ICollectiveTaskLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class ITaskContent(model.Schema):
    """ Interface for task content type """

    title = schema.TextLine(
        title=_PMF(u'label_title', default=u'Title'),
        required=True
    )


class ITaskMethods(Interface):

    def get_highest_task_parent(task=False):
        """
            Get the object containing the highest ITask object
            or the highest ITask object if task is True
        """

