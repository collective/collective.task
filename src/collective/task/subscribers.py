# -*- coding: utf-8 -*-

from collective.task.adapters import TaskContentAdapter
from collective.task.interfaces import ITaskContent


def afterTransitionITaskSubscriber(obj, event):
    """ After transition subscribers on ITask"""

    if event.transition and event.transition.id == 'do_to_assign':
        # Set auto_to_do_flag on task if assigned_user is set.
        if obj.assigned_user:
            obj.auto_to_do_flag = True
        else:
            obj.auto_to_do_flag = False

    if event.transition and event.transition.id == 'back_in_to_assign':
        # Remove auto_to_do_flag on task.
        obj.auto_to_do_flag = False


def taskContent_created(task, event):
    """
        Update parents localrole fields.
        Moving a tree will trigger events from children to parents !
    """
    if event.oldParent is None or event.oldName is None:
        status = 'creation'
    elif event.oldParent != event.newParent:
        status = 'move'
    elif event.oldName != event.newName:
        status = 'rename'
        return
    print "MOVED %s on %s" % (status, task.absolute_url_path())
    adapted = TaskContentAdapter(task)
    if status == 'move':
        adapted.set_all_parents_value('parents_assigned_groups', 'get_parents_assigned_groups')

    adapted.set_parents_value('parents_assigned_groups', adapted.get_parents_assigned_groups(), modified=False)
