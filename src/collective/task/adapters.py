# -*- coding: utf-8 -*-

from collective.task.behaviors import ITask
from collective.task.interfaces import ITaskContent
from collective.task.interfaces import ITaskMethods
from datetime import date
from plone.indexer import indexer
from plone.registry.interfaces import IRegistry
from Products.CMFCore.interfaces import IContentish
from Products.CMFPlone.utils import base_hasattr
from Products.PluginIndexes.common.UnIndex import _marker as common_marker
from Products.PluginIndexes.DateIndex.DateIndex import _marker as date_marker
from zope.component import adapts
from zope.component import getUtility
from zope.dottedname.resolve import resolve
from zope.interface import implements


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


class ParentsBaseAdapter(object):

    def __init__(self, context):
        self.context = context

    def get_parents_fields(self):
        registry = getUtility(IRegistry)
        ret = {}
        for dic in registry.get('collective.task.parents_fields', []):
            if dic['fieldname'] not in ret:
                ret[dic['fieldname']] = []
            ret[dic['fieldname']].append({'at': dic['attribute'], 'prefix': dic['attribute_prefix'] or '',
                                          'p_if': resolve(dic['provided_interface'])})
        return ret


class TaskContainerAdapter(ParentsBaseAdapter):
    """
        implements(ITaskContainerMethods)
        adapts(ITaskContainer)
    """

    def get_taskcontent_children(self):
        brains = self.context.portal_catalog(portal_type='task', path='/'.join(self.context.getPhysicalPath()),
                                             sort_on='path')
        objs = [b.getObject() for b in brains]
        if objs and objs[0] == self.context:
            return objs[1:]
        return objs

    def set_lower_parents_value(self, attr, dic):
        # we refresh all tree lower
        children = self.get_taskcontent_children()
        for obj in children:
            adapted = TaskContentAdapter(obj)
            adapted.set_parents_value(attr, adapted.calculate_parents_value(attr, dic))


class TaskContentAdapter(ParentsBaseAdapter):
    """
        implements(ITaskContentMethods)
        adapts(ITaskContent)
    """

    def calculate_parents_value(self, field, p_fields):
        """ Calculate parents_... field on direct parent """
        obj = self.context
        parent = obj.aq_parent
        new_value = []
        for dic in p_fields:
            if dic['p_if'].providedBy(parent):
                if base_hasattr(parent, field) and getattr(parent, field):
                    new_value += [val for val in getattr(parent, field) if val not in new_value]
                # we add parent field value
                parent_value = base_hasattr(parent, dic['at']) and getattr(parent, dic['at']) or None
                if parent_value and parent_value not in new_value:
                    new_value.append(parent_value)
        return new_value

    def set_parents_value(self, attr, value, modified=False):
        if value:
            setattr(self.context, attr, value)
            if modified:
                modified(self.context)
            return value
        return None

    def get_taskcontent_parents(self, ifs=[ITaskContent]):
        parents = []
        parent = self.context.aq_parent
        for intf in ifs:
            while parent is not None:
                if intf.providedBy(parent):
                    parents.append(parent)
                    parent = parent.aq_parent
                else:
                    parent = None
        parents.reverse()
        return parents

    def set_higher_parents_value(self, attr, p_fields):
        # we refresh all tree upper
        parents = self.get_taskcontent_parents()
        for obj in parents:
            adapted = TaskContentAdapter(obj)
            adapted.set_parents_value(attr, adapted.calculate_parents_value(attr, p_fields))
