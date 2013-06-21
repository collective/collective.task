# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from plone.theme.interfaces import IDefaultPloneLayer


class ICollectiveTaskLayer(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer."""


class IBaseTask(model.Schema):
    """Marker interface for all "tasks" content types"""
    pass
