# -*- coding: utf-8 -*-
"""Custom viewlets."""
from plone import api
from plone.app.layout.viewlets import common as base

from collective.task.behaviors import ITask
from collective.task.browser.table import TasksTable
from collective.task import _


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
