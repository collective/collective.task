# -*- coding: utf-8 -*-
"""Subscribers."""


def set_auto_to_do_flag(obj, event):
    """Set auto_to_do_flag on task if assigned_user is set."""
    if event.transition and event.transition.id == 'do_to_assign':
        if obj.assigned_user:
            obj.auto_to_do_flag = True
        else:
            obj.auto_to_do_flag = False


def remove_auto_to_do_flag(obj, event):
    """Remove auto_to_do_flag on task if assigned_user is set."""
    if event.transition and event.transition.id == 'back_in_to_assign':
        obj.auto_to_do_flag = False
