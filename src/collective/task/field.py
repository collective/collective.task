# -*- coding: utf-8 -*-
"""Define custom fields."""
from collective.task.interfaces import ILocalRoleMasterSelectField
from dexterity.localrolesfield.field import LocalRoleField
from plone.formwidget.masterselect import MasterSelectField
from zope.interface import implementer

import plone.supermodel.exportimport


@implementer(ILocalRoleMasterSelectField)
class LocalRoleMasterSelectField(LocalRoleField, MasterSelectField):

    """Local role single value field which can be used as a master select."""


LocalRoleSelectHandler = plone.supermodel.exportimport.ChoiceHandler(LocalRoleMasterSelectField)
LocalRoleHandler = plone.supermodel.exportimport.ChoiceHandler(LocalRoleField)
