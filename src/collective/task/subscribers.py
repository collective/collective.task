# -*- coding: utf-8 -*-

from collective.task.interfaces import ITaskContainerMethods
from collective.task.interfaces import ITaskContentMethods
from zope.component import getAdapter


def afterTransitionITaskSubscriber(obj, event):
    """After transition subscribers on ITask"""

    if event.transition and event.transition.id == "do_to_assign":
        # Set auto_to_do_flag on task if assigned_user is set.
        if obj.assigned_user:
            obj.auto_to_do_flag = True
        else:
            obj.auto_to_do_flag = False

    if event.transition and event.transition.id == "back_in_to_assign":
        # Remove auto_to_do_flag on task.
        obj.auto_to_do_flag = False


def taskContent_created(task, event):
    """
    Update parents localrole fields.
    Moving or copying a tree will trigger events from children to parents !
    """
    # print "op:%s, on:%s, np:%s, nn:%s" % (event.oldParent, event.oldName, event.newParent, event.newName)
    if event.oldParent is None or event.oldName is None:
        status = "create"
    elif event.newParent is None or event.newName is None:
        status = "delete"
        return
    elif event.oldParent != event.newParent:
        status = "move"
    elif event.oldName != event.newName:
        status = "rename"
        return
    status
    # print "MOVED %s on %s" % (status, task.absolute_url_path())
    adapted = getAdapter(task, ITaskContentMethods)
    fields = adapted.get_parents_fields()
    for field in fields:
        # update all higher tree: needed when moving or copying
        adapted.set_higher_parents_value(field, fields[field])
        # update current
        adapted.set_parents_value(field, adapted.calculate_parents_value(field, fields[field]))


def taskContent_modified(task, event):
    """
    Update parents localrole fields.
    """
    # print "MODIF %s with %s" % (task.absolute_url_path(), ';'.join([str(e.interface) for e in event.descriptions]))
    # at object creation
    if not event.descriptions:
        return
    updates = []
    adapted = getAdapter(task, ITaskContainerMethods)
    fields = adapted.get_parents_fields()
    for at in event.descriptions:
        for field in fields:
            for dic in fields[field]:
                fieldname = dic["prefix"] and "%s.%s" % (dic["prefix"], dic["at"]) or dic["at"]
                if fieldname in at.attributes:
                    updates.append(field)
                    break
    for field in updates:
        adapted.set_lower_parents_value(field, fields[field])
