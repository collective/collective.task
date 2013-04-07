from five import grok

from z3c.form import button
from z3c.form.field import Fields
from z3c.form.interfaces import HIDDEN_MODE
from zope import schema

from Acquisition import aq_inner, aq_chain

from plone import api
from plone.dexterity.browser.add import DefaultAddForm
from plone.dexterity.i18n import MessageFactory as DMF
from plone.supermodel import model

from Products.CMFPlone.utils import base_hasattr
from Products.statusmessages.interfaces import IStatusMessage

from collective.task.content.task import ITask

from collective.task import _


def find_nontask(obj):
    """Find the first non task object in acquisition chain"""
    for item in aq_chain(aq_inner(obj)):
        if base_hasattr(item, 'portal_type'):
            if item.portal_type != 'task':
                return item
        else:
            return item


class IWorkflowAction(model.Schema):
    """Simple schema that contains workflow action hidden field"""
    workflow_action = schema.TextLine(title=_(u'Workflow action'),
                                      required=False
                                      )

class AttributeTask(DefaultAddForm):
    """When an "Attribute" transition is triggered,
    create a new subtask
    """
    description = u""
    schema = ITask
    portal_type = 'task'
    fields = Fields(ITask)
    fields += Fields(IWorkflowAction)
    fields['workflow_action'].mode = HIDDEN_MODE

    def updateWidgets(self):
        """Update widgets then add workflow_action value to workflow_action field"""
        super(AttributeTask, self).updateWidgets()
        if 'workflow_action' in self.request:
            self.widgets['workflow_action'].value = (
                self.request['workflow_action'])
        self.widgets['title'].value = self.context.title
        if self.context.deadline is not None:
            deadline = (str(self.context.deadline.year),
                        str(self.context.deadline.month),
                        str(self.context.deadline.day))
            self.widgets['deadline'].value = deadline

    @button.buttonAndHandler(_('Add'), name='save')
    def handleAdd(self, action):
        """When the subtask is added,
        grant Reviewer role to current user on new object
        Then, execute transition on container
        """
        parent_task = aq_inner(self.context)
        container_url = parent_task.absolute_url()
        data, errors = self.extractData()
        workflow_action = data['workflow_action']
        del data['workflow_action']
        if errors:
            self.status = self.formErrorsMessage
            return
        obj = self.createAndAdd(data)
        if obj is not None:
            supervisor = parent_task.responsible[0]
            # mark only as finished if we get the new object
            self._finishedAdd = True
            IStatusMessage(self.request).addStatusMessage(DMF(u"Item created"), "info")
            # set Reviewer role on new object to the current user
            obj.manage_addLocalRoles(supervisor, ['Reviewer',])
            obj.reindexObject()
            # set Editor role to task responsible on the first non Task object in acquisition
            nontask = find_nontask(parent_task)
            nontask.manage_addLocalRoles(obj.responsible[0], ['Editor',])
            nontask.reindexObject()
            self.immediate_view = "%s/content_status_modify?workflow_action=%s" % (container_url, workflow_action)
