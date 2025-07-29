# -*- coding: utf-8 -*-
"""Example."""
from .behaviors import ITaskContainer
from Acquisition import aq_inner
from Acquisition import aq_parent
from dexterity.localroles.interfaces import ILocalRolesRelatedSearchUtility
from plone import api
from zope.interface import implementer


@implementer(ILocalRolesRelatedSearchUtility)
class TaskContainerRelatedSearch(object):
    """TaskContainer related search."""

    def get_objects(self, obj):
        """Return the parents if they are TaskContainer."""
        ret = []
        parent = aq_parent(aq_inner(obj))
        while ITaskContainer.providedBy(parent):
            ret.append(parent)
            if parent == api.portal.getSite():
                break
            parent = aq_parent(aq_inner(parent))
        return ret
