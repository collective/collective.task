# -*- coding: utf-8 -*-


def afterTransitionITaskSubscriber(obj, event):
    """ After transition subscribers on ITask"""

    if event.transition and event.transition.id == 'do_to_assign':
        # Set auto_to_do_flag on task if assigned_user is set.
        if obj.assigned_user:
            obj.auto_to_do_flag = True
        else:
            obj.auto_to_do_flag = False

    if event.transition and event.transition.id == 'back_in_to_assign':
        # Remove auto_to_do_flag on task if assigned_user is set.
        obj.auto_to_do_flag = False
