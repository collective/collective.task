# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from plone.dexterity.content import IDexterityContainer


class ICollectiveTaskLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class ITaskContent(IDexterityContainer):
    """ Interface for task content type """
