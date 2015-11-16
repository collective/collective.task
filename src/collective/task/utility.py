# -*- coding: utf-8 -*-
"""Example."""
from Acquisition import aq_inner, aq_parent
from zope.interface import implements

from plone import api
from dexterity.localroles.interfaces import ILocalRolesRelatedSearchUtility

from .behaviors import ITaskContainer


class TaskContainerRelatedSearch(object):
    """ TaskContainer related search. """

    implements(ILocalRolesRelatedSearchUtility)

    def get_objects(self, obj):
        """ Return the parents if they are TaskContainer. """
        ret = []
        parent = aq_parent(aq_inner(obj))
        while(ITaskContainer.providedBy(parent)):
            ret.append(parent)
            if parent == api.portal.getSite():
                break
            parent = aq_parent(aq_inner(parent))
        return ret
