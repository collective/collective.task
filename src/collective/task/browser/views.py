# -*- coding: utf-8 -*-

from collective.task import _
from plone import api
from plone.app import dexterity
from plone.dexterity.browser.view import DefaultView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

import copy


class TaskItemView(DefaultView):
    """Task view using item template for IDexterityContainer"""

    index = ViewPageTemplateFile("%s/browser/item.pt" % dexterity.__path__[0])

    def updateWidgets(self):
        super(TaskItemView, self).updateWidgets()
        if not self.context.assigned_user and api.content.get_state(obj=self.context) == "to_assign":
            self.widgets["ITask.assigned_user"].field = copy.copy(self.widgets["ITask.assigned_user"].field)
            self.widgets["ITask.assigned_user"].field.description = _(
                u"You must select an assigned user before continuing !"
            )
