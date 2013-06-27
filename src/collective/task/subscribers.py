from five import grok

from zope.lifecycleevent.interfaces import IObjectRemovedEvent,\
    IObjectAddedEvent

from plone import api
from Products.DCWorkflow.interfaces import IAfterTransitionEvent

from collective.z3cform.rolefield.field import LocalRolesToPrincipalsDataManager

from collective.task.behaviors import ITarget
from collective.task.content.task import ITask
from collective.task.content.opinion import IOpinion
from collective.task.content.validation import IValidation
from collective.task.interfaces import IBaseTask


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


@grok.subscribe(ITarget, IObjectAddedEvent)
def set_reader_on_target(context, event):
    """Set Reader role on target to responsible after opinion or validation creation"""
    target = context.target.to_object
    responsible = context.responsible[0]
    api.user.grant_roles(username=responsible, roles=['Reader'], obj=target)

@grok.subscribe(IValidation, IObjectAddedEvent)
def set_reviewer_on_target(context, event):
    """Set Reviewer role on target to responsible after validation creation"""
    target = context.target.to_object
    responsible = context.responsible[0]
    api.user.grant_roles(username=responsible, roles=['Reviewer'], obj=target)
