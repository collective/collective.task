# -*- coding: utf-8 -*-
"""Behaviors."""
from zope.interface import alsoProvides
from zope import schema

from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model

from dexterity.localrolesfield.field import LocalRolesField

from collective.task import _


class ITask(model.Schema):

    """ITask behavior."""

    assigned_group = LocalRolesField(
        title=_(u"Assigned group"),
        required=False,
        value_type=schema.Choice(
            vocabulary="plone.principalsource.Groups")
        )

    assigned_user = LocalRolesField(
        title=_(u"Assigned user"),
        required=False,
        value_type=schema.Choice(
            vocabulary="plone.principalsource.Users")
        )

    enquirer = schema.TextLine(
        title=_(u"Enquirer"),
        required=False,
        )

    due_date = schema.Date(
        title=_(u"Due date"),
        required=False,
        )


alsoProvides(ITask, IFormFieldProvider)
