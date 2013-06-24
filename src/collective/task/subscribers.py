from five import grok

from zope.lifecycleevent.interfaces import IObjectRemovedEvent,\
    IObjectAddedEvent

from plone import api
from Products.DCWorkflow.interfaces import IAfterTransitionEvent

from collective.z3cform.rolefield.field import LocalRolesToPrincipalsDataManager

from collective.task.content.task import ITask
from collective.task.interfaces import IBaseTask
from collective.task.content.opinion import IOpinion
from collective.task.content.validation import IValidation
from collective.dms.basecontent.dmsdocument import IDmsDocument


@grok.subscribe(ITask, IAfterTransitionEvent)
def task_changed_state(context, event):
    """When a task is abandoned or done, check if it is a subtask
    and make the wanted transition to parent
    """
    parent = context.getParentNode()
    if parent.portal_type == 'task':
        with api.env.adopt_roles(['Reviewer']):
            if event.new_state.id == 'done':
                api.content.transition(obj=parent, transition='subtask-done')
            elif event.new_state.id == 'abandoned':
                api.content.transition(obj=parent, transition='subtask-abandoned')


@grok.subscribe(ITask, IObjectRemovedEvent)
def reopen_parent_task(context, event):
    """When a task is deleted, reopen its parent task
    """
    parent = context.getParentNode()
    parent_state = api.content.get_state(parent)
    if parent.portal_type == 'task' and parent_state == 'attributed':
        with api.env.adopt_roles(['Reviewer']):
            api.content.transition(obj=parent, transition='subtask-abandoned')


@grok.subscribe(IBaseTask, IObjectAddedEvent)
def set_enquirer(context, event):
    """Set Enquirer field after task creation"""
    enquirer = api.user.get_current().id
    enquirer_dm = LocalRolesToPrincipalsDataManager(context, IBaseTask['enquirer'])
    enquirer_dm.set((enquirer,))


@grok.subscribe(IBaseTask, IObjectAddedEvent)
def set_role_on_document(context, event):
    if not ITask.providedBy(context):
        document = context.getParentNode()  # do we need to use aq_inner here ?
        cansee_dm = LocalRolesToPrincipalsDataManager(document, IDmsDocument['recipient_groups'])
        cansee_dm.set(tuple(context.responsible))
    # do we have to set Editor role on document for ITask ? (if so, remove something for IDmsMail ?)


@grok.subscribe(IOpinion, IObjectAddedEvent)
def set_editor_on_version(context, event):
    """Set Editor role on version to responsible after opinion creation"""
    version = context.version
    import pdb;pdb.set_trace()
    responsible = context.responsible
    api.user.grant_roles(user=responsible, roles=['Editor'], obj=version)


@grok.subscribe(IValidation, IObjectAddedEvent)
def set_reader_on_version(context, event):
    """Set Reader role on version to responsible after validation creation"""
    version = context.version
    responsible = context.responsible
    api.user.grant_roles(user=responsible, roles=['Reader'], obj=version)

