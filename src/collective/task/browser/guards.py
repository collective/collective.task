from five import grok

from plone import api

from collective.task.content.task import ITask


class BaseSubtaskGuard(grok.View):
    """Base class for 'subtask' guards views"""
    grok.context(ITask)
    grok.baseclass()
    grok.require("zope2.View")

    def update(self):
        """Create subtasks states list"""
        subtasks = self.context.listFolderContents()
        self.subtasks_states = [api.content.get_state(subtask) for subtask in subtasks]


class SubtaskDoneGuard(BaseSubtaskGuard):
    """Returns True if the subtask is done"""
    grok.name("subtask_done")

    def render(self):
        return 'done' in self.subtasks_states


class SubtasksAbandonedGuard(BaseSubtaskGuard):
    """Returns True is the subtask is abandoned"""
    grok.name("subtasks_abandoned")

    def render(self):
        return set(['abandoned']) == set(self.subtasks_states)
