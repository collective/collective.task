# -*- coding: utf-8 -*-

from datetime import date
from zope.component import adapts
from zope.interface import implements
from zope.lifecycleevent import modified

from plone.indexer import indexer
from Products.CMFCore.interfaces import IContentish
from Products.CMFPlone.utils import base_hasattr
from Products.PluginIndexes.common.UnIndex import _marker as common_marker
from Products.PluginIndexes.DateIndex.DateIndex import _marker as date_marker

from .behaviors import ITask
from .interfaces import ITaskMethods, ITaskContent, ITaskContentMethods

EMPTY_STRING = '__empty_string__'
EMPTY_DATE = date(1950, 1, 1)


@indexer(IContentish)
def assigned_group_index(obj):
    """ Index method escaping acquisition """
    if base_hasattr(obj, 'assigned_group') and obj.assigned_group:
        return obj.assigned_group
    return common_marker


@indexer(IContentish)
def assigned_user_index(obj):
    """ Index method escaping acquisition """
    if base_hasattr(obj, 'assigned_user'):
        if obj.assigned_user:
            return obj.assigned_user
        else:
            # set value in index for null content to find in catalog null content
            return EMPTY_STRING
    return common_marker


@indexer(IContentish)
def due_date_index(obj):
    """ Index method escaping acquisition """
    if base_hasattr(obj, 'due_date'):
        if obj.due_date:
            return obj.due_date
        else:
            # set value in index for null content to find in catalog null content
            return EMPTY_DATE
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
            # if not hasattr(obj, "aq_parent"):
            #     raise RuntimeError("Parent traversing interrupted by object: " + str(obj))
            parent = obj.aq_parent
            if not ITask.providedBy(parent):
                if task:  # we want the highest task, we return the current task obj
                    return obj
                else:  # we return the parent that's not a task
                    return parent
            obj = parent
        return obj

    def get_full_tree_title(self):
        """Returns the full title of the task tree
           It is constituted by the list of the names of the tasks and parent task separated by slashes
           e.g. for Bar task in Foo task : u" Foo/Bare
        """
        obj = self.context
        full_tree_title = obj.Title()
        while ITask.providedBy(obj.aq_parent):
            full_tree_title = obj.aq_parent.Title() + ' / ' + full_tree_title
            obj = obj.aq_parent
        return full_tree_title


class TaskContentAdapter(object):
    implements(ITaskContentMethods)
    adapts(ITaskContent)

    def __init__(self, context):
        self.context = context

    def calculate_pag(self):
        """ Calculate parents_assigned_groups on direct parent """
        obj = self.context
        parent = obj.aq_parent
        new_value = []
        if ITaskContent.providedBy(parent):
            if parent.parents_assigned_groups:
                # slicing to create a copy and not a reference
                new_value = parent.parents_assigned_groups[:]
            if parent.assigned_group and parent.assigned_group not in new_value:
                new_value.append(parent.assigned_group)
        return new_value

    def set_parents_value(self, attr, value, modified=True):
        if value:
            setattr(self.context, attr, value)
            if modified:
                modified(self.context)
            return value
        return None

    def set_higher_parents_value(self, attr, getter):
        # we refresh all tree upper
        parents = []
        parent = self.context.aq_parent
        while parent is not None:
            if ITaskContent.providedBy(parent):
                parents.append(parent)
                parent = parent.aq_parent
            else:
                parent = None
        parents = reversed(parents)
        for obj in parents:
            adapted = TaskContentAdapter(obj)
            method = getattr(adapted, getter)
            adapted.set_parents_value(attr, method(), modified=False)
