# -*- coding: utf-8 -*-

from zope.component import adapts
from zope.interface import implements

from plone.indexer import indexer
from Products.CMFCore.interfaces import IContentish
from Products.CMFPlone.utils import base_hasattr
from Products.PluginIndexes.common.UnIndex import _marker as common_marker
from Products.PluginIndexes.DateIndex.DateIndex import _marker as date_marker

from .behaviors import ITask
from.interfaces import ITaskMethods


@indexer(IContentish)
def assigned_group_index(obj):
    """ Index method escaping acquisition """
    if base_hasattr(obj, 'assigned_group') and obj.assigned_group:
        return obj.assigned_group
    return common_marker


@indexer(IContentish)
def assigned_user_index(obj):
    """ Index method escaping acquisition """
    if base_hasattr(obj, 'assigned_user') and obj.assigned_user:
        return obj.assigned_user
    return common_marker


@indexer(IContentish)
def due_date_index(obj):
    """ Index method escaping acquisition """
    if base_hasattr(obj, 'due_date') and obj.due_date:
        return obj.due_date
    return date_marker


class TaskAdapter(object):
    implements(ITaskMethods)
    adapts(ITask)

    def __init__(self, context):
        self.context = context

    def get_highest_task_parent(self, task=False):
        """
            Get the object containing the highest ITask object
            or the highest ITask object if task is True
        """
        obj = self.context
        while obj is not None:
#            if not hasattr(obj, "aq_parent"):
#                raise RuntimeError("Parent traversing interrupted by object: " + str(obj))
            parent = obj.aq_parent
            if not ITask.providedBy(parent):
                if task:  # we want the highest task, we return the current task obj
                    return obj
                else:  # we return the parent that's not a task
                    return parent
            obj = parent
        return obj
