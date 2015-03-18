# -*- coding: utf-8 -*-
"""Define custom fields."""
from plone.formwidget.masterselect import MasterSelectField

from dexterity.localrolesfield.field import LocalRoleField


class LocalRoleMasterSelectField(LocalRoleField, MasterSelectField):

    """Local role single value field which can be used as a master select."""
