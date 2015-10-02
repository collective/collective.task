# -*- coding: utf-8 -*-

from plone import api
from plone.app import dexterity
from plone.dexterity.browser.view import DefaultView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from .. import _


class TaskItemView(DefaultView):
    """ Task view using item template for IDexterityContainer """

    index = ViewPageTemplateFile("%s/browser/item.pt" % dexterity.__path__[0])

    def updateWidgets(self):
        super(TaskItemView, self).updateWidgets()
        if not self.context.assigned_user \
                and api.content.get_state(obj=self.context) == 'to_assign':
            self.widgets['ITask.assigned_user'].field.description = \
                _(u'You must select an assigned user before continuing !')
        else:
            self.widgets['ITask.assigned_user'].field.description = u''
