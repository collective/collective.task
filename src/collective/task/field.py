# -*- coding: utf-8 -*-
"""Define custom fields."""

from dexterity.localrolesfield.field import LocalRoleField
from plone.formwidget.masterselect import MasterSelectField

import plone.supermodel.exportimport


class LocalRoleMasterSelectField(LocalRoleField, MasterSelectField):

    """Local role single value field which can be used as a master select."""

LocalRoleSelectHandler = plone.supermodel.exportimport.ChoiceHandler(LocalRoleMasterSelectField)
LocalRoleHandler = plone.supermodel.exportimport.ChoiceHandler(LocalRoleField)
