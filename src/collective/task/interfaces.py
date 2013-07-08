# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""
from z3c.form.browser.select import SelectFieldWidget
from zope import schema

from plone.autoform import directives as form
from plone.formwidget.datetime.z3cform.widget import DatetimeFieldWidget
from plone.supermodel import model
from plone.theme.interfaces import IDefaultPloneLayer

from collective.z3cform.chosen.widget import ChosenMultiFieldWidget
from collective.z3cform.rolefield.field import LocalRolesToPrincipals

from collective.task import _


class ICollectiveTaskLayer(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer."""


class IBaseTask(model.Schema):
    """Interface for all "tasks" content types"""
    title = schema.TextLine(title=_(u'Title'))
    note = schema.Text(title=_(u'Note'),
                       required=False)
    deadline = schema.Datetime(title=_(u'Deadline'),
                               required=False)
    form.widget(deadline=DatetimeFieldWidget)

    enquirer = LocalRolesToPrincipals(
        title=_(u"Enquirer"),
        roles_to_assign=('Reviewer',),
        value_type=schema.Choice(
            vocabulary="plone.principalsource.Principals"
        ),
        min_length=0,
        max_length=1,
        required=False,
    )
    form.widget(enquirer=SelectFieldWidget)
    form.mode(enquirer='hidden')

    responsible = LocalRolesToPrincipals(
        title=_(u"Addressee"),
        roles_to_assign=('Editor',),
        value_type=schema.Choice(
            vocabulary="plone.principalsource.Principals"
        ),
        min_length=1,
        max_length=1,
        required=True,
    )
    form.widget(responsible=ChosenMultiFieldWidget)

    form.order_after(note='responsible')
