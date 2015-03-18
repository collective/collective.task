# -*- coding: utf-8 -*-
"""Behaviors."""
from zope.interface import alsoProvides, Interface
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone import api
from plone.autoform.interfaces import IFormFieldProvider
from plone.directives.form.value import default_value
from plone.supermodel import model
from plone.supermodel.directives import fieldset

from dexterity.localrolesfield.field import LocalRoleField

from collective.task.field import LocalRoleMasterSelectField
from collective.task import _


def get_users_vocabulary(group):
    """Get users vocabulary when an assigned group is selected."""
    # return GroupMembersSourceBinder(groupname=group)
    terms = []
    try:
        members = api.user.get_users(groupname=group)
        for member in members:
            member_id = member.getId()
            title = member.getUser().getProperty('fullname') or member_id
            terms.append(SimpleTerm(
                value=member.getUserName(),  # login
                token=member_id,  # id
                title=title))  # title
    except api.exc.GroupNotFoundError:
        pass

    return SimpleVocabulary(terms)


class ITaskContainer(Interface):

    """Marker interface for task containers."""


class ITask(model.Schema):

    """ITask behavior."""

    assigned_group = LocalRoleMasterSelectField(
        title=_(u"Assigned group"),
        required=False,
        vocabulary="plone.principalsource.Groups",
        slave_fields=(
            {'name': 'ITask.assigned_user',
             'slaveID': '#form-widgets-ITask-assigned_user',
             'action': 'vocabulary',
             'vocab_method': get_users_vocabulary,
             'control_param': 'group',
            },
            )
        )

    assigned_user = LocalRoleField(
        title=_(u"Assigned user"),
        required=False,
        vocabulary="plone.principalsource.Users"
        )

    enquirer = schema.Choice(
        title=_(u"Enquirer"),
        required=False,
        vocabulary="plone.principalsource.Users"
        )

    due_date = schema.Date(
        title=_(u"Due date"),
        required=False,
        )


class ITaskWithFieldset(ITask):

    """ITask behavior with fieldset."""

    fieldset(
        'task',
        label=_(u'Task'),
        fields=('assigned_group', 'assigned_user', 'enquirer', 'due_date',)
        )


@default_value(field=ITask['enquirer'])
def get_current_user_id(data):
    """Current user by default."""
    current_user = api.user.get_current()
    if current_user:
        return current_user.getId()

    return ""


alsoProvides(ITask, IFormFieldProvider)
