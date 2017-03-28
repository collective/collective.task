# -*- coding: utf-8 -*-

from collective.task.adapters import TaskContentAdapter


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
        Moving or copying a tree will trigger events from children to parents !
    """
    #print "op:%s, on:%s, np:%s, nn:%s" % (event.oldParent, event.oldName, event.newParent, event.newName)
    if event.oldParent is None or event.oldName is None:
        status = 'create'
    elif event.newParent is None or event.newName is None:
        status = 'delete'
        return
    elif event.oldParent != event.newParent:
        status = 'move'
    elif event.oldName != event.newName:
        status = 'rename'
        return
    #print "MOVED %s on %s" % (status, task.absolute_url_path())
    adapted = TaskContentAdapter(task)
    # update all higher tree: needed when moving or copying
    adapted.set_higher_parents_value('parents_assigned_groups', 'assigned_group')
    # update current
    adapted.set_parents_value('parents_assigned_groups',
                              adapted.calculate_parents_value('parents_assigned_groups', 'assigned_group'))


def taskContent_modified(task, event):
    """
        Update parents localrole fields.
    """
    #print "MODIF %s with %s" % (task.absolute_url_path(), ';'.join([str(e.interface) for e in event.descriptions]))
    adapted = TaskContentAdapter(task)
    # at object creation
    if not event.descriptions:
        return
    update = False
    for at in event.descriptions:
        if 'ITask.assigned_group' in at.attributes:
            update = True
            break
    if update:
        adapted.set_lower_parents_value('parents_assigned_groups', 'assigned_group')
