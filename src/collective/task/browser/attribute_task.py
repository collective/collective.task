from z3c.form import button
from z3c.form.field import Fields
from z3c.form.interfaces import HIDDEN_MODE
from zope import schema

from Acquisition import aq_inner

from plone import api
from plone.dexterity.browser.add import DefaultAddForm
from plone.dexterity.i18n import MessageFactory as DMF
from plone.supermodel import model

from Products.statusmessages.interfaces import IStatusMessage

from collective.task.content.task import ITask

from collective.task import _


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

    @button.buttonAndHandler(_('Add'), name='save')
    def handleAdd(self, action):
        """When the subtask is added,
        grant Reviewer role to current user on new object
        Then, execute transition on container
        """
        container_url = aq_inner(self.context).absolute_url()
        data, errors = self.extractData()
        workflow_action = data['workflow_action']
        del data['workflow_action']
        if errors:
            self.status = self.formErrorsMessage
            return
        obj = self.createAndAdd(data)
        if obj is not None:
            # mark only as finished if we get the new object
            self._finishedAdd = True
            IStatusMessage(self.request).addStatusMessage(DMF(u"Item created"), "info")
            # set Reviewer role on new object to the current user
            parent_task_editor = api.user.get_current()
            api.user.grant_roles(user=parent_task_editor, obj=obj, roles=['Reviewer',])
            self.immediate_view = "%s/content_status_modify?workflow_action=%s" % (container_url, workflow_action)
