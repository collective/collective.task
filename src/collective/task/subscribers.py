from five import grok

from zope.lifecycleevent.interfaces import IObjectRemovedEvent

from plone import api

from collective.task.content.task import ITask


@grok.subscribe(ITask, IObjectRemovedEvent)
def reopen_parent_task(context, event):
    """When a task is deleted, reopen its parent task
    """
    parent = context.getParentNode()
    parent_state = api.content.get_state(parent)
    if parent.portal_type == 'task' and parent_state == 'attributed':
        with api.env.adopt_roles(['Reviewer']):
            api.content.transition(obj=parent, transition='subtask-abandoned')
