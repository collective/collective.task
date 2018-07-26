# -*- coding: utf-8 -*-
"""Custom viewlets."""
from collective.task import _
from collective.task.behaviors import ITask
from collective.task.interfaces import ITaskMethods
from plone import api
from plone.app.layout.viewlets import common as base
from table import TasksTable


class TasksListViewlet(base.ViewletBase):

    """Tasks list for current task container object."""

    label = _(u"Tasks list")
    noresult_message = _(u"There is no task for this content.")
    __table__ = TasksTable

    def update(self):
        self.table = self.__table__(self.context, self.request)
        self.table.viewlet = self
        catalog = api.portal.get_tool('portal_catalog')
        container_path = '/'.join(self.context.getPhysicalPath())
        brains = catalog.searchResults(
            object_provides=ITask.__identifier__,
            path={'query': container_path, 'depth': 1})
        self.table.results = [b.getObject() for b in brains]
        self.table.update()


class TaskParentViewlet(base.ViewletBase):

    """Task parent for current task."""

    display_highest_task = True
    display_above_element = True

    def get_highest_parent(self):
        """ Return highest task and above task chain """
        ret = {'highest': None, 'above': None}
        parent_task = ITaskMethods(self.context).get_highest_task_parent(task=True)
        if self.display_highest_task and parent_task != self.context:
            ret['highest'] = parent_task
        if self.display_above_element:
            ret['above'] = parent_task.aq_parent
        return ret
