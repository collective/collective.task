from five import grok

from zope.lifecycleevent.interfaces import IObjectRemovedEvent

from plone import api
from Products.DCWorkflow.interfaces import IAfterTransitionEvent

from collective.task.content.task import ITask


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
