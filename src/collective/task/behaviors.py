# -*- coding: utf-8 -*-
"""Behaviors."""

try:
    from zope.schema.interfaces import IVocabularyFactory
except ImportError:
    from zope.app.schema.vocabulary import IVocabularyFactory

from collective.task import _
from collective.task.field import LocalRoleMasterSelectField
from dexterity.localrolesfield.field import LocalRoleField
from plone import api
from plone.app.textfield import RichText
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.browser.edit import DefaultEditForm
from plone.supermodel import model
from plone.supermodel.directives import fieldset
from z3c.form import validator
from zope import schema
from zope.component import getUtility
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import Invalid
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

import datetime


try:
    from plone.base.utils import base_hasattr
except ImportError:
    from Products.CMFPlone.utils import base_hasattr


now = datetime.datetime.today()


@implementer(IVocabularyFactory)
class AssignedGroupsVocabulary(object):
    """Define own factory and named utility that can be easily overrided in componentregistry.xml"""

    def __call__(self, context):
        return SimpleVocabulary.fromValues([g.getGroupName() for g in api.group.get_groups()])


AssignedGroupsVocabularyFactory = AssignedGroupsVocabulary()


@implementer(IVocabularyFactory)
class AssignedUsersVocabulary(object):
    """Define own factory and named utility that can be easily overrided in componentregistry.xml"""

    def __call__(self, context):
        voc = getUtility(IVocabularyFactory, name="imio.helpers.SimplySortedUsers", context=context)
        return voc(context)


AssignedUsersVocabularyFactory = AssignedUsersVocabulary()


@implementer(IVocabularyFactory)
class EnquirerVocabulary(object):
    """Define own factory and named utility that can be easily overrided in componentregistry.xml"""

    def __call__(self, context):
        voc = getUtility(IVocabularyFactory, name="imio.helpers.SimplySortedUsers", context=context)
        return voc(context)


EnquirerVocabularyFactory = EnquirerVocabulary()


def get_users_vocabulary(group):
    """Get users vocabulary when an assigned group is selected."""
    terms = []
    try:
        members = api.user.get_users(groupname=group)
        for member in members:
            member_id = member.getId()
            title = member.getUser().getProperty("fullname") or member_id
            terms.append(SimpleTerm(value=member.getUserName(), token=member_id, title=title))  # login  # id  # title
    except api.exc.GroupNotFoundError:
        pass

    return SimpleVocabulary(terms)


@provider(IContextAwareDefaultFactory)
def get_parent_assigned_group(context):
    """If parent has assigned_group, set it as default value"""
    # Are we in add form ?
    if not context.REQUEST.get("PATH_INFO", "/").split("/")[-1].startswith("++add++"):
        return None
    if base_hasattr(context, "assigned_group") and context.assigned_group:
        return context.assigned_group
    return None


def get_current_user_id():
    """Current user by default."""
    current_user = api.user.get_current()
    if current_user:
        return current_user.getId()
    return None


class ITaskContainer(Interface):

    """Marker interface for task containers."""


class ITask(model.Schema):

    """ITask behavior."""

    task_description = RichText(
        title=_(u"Task description"),
        required=False,
        description=_(u"What is to do and/or what is done"),
        allowed_mime_types=(u"text/html",),
    )

    assigned_group = LocalRoleMasterSelectField(
        title=_(u"Assigned group"),
        required=False,
        vocabulary="collective.task.AssignedGroups",
        slave_fields=(
            {
                "name": "ITask.assigned_user",
                "slaveID": "#form-widgets-ITask-assigned_user",
                "action": "vocabulary",
                "vocab_method": get_users_vocabulary,
                "control_param": "group",
                "initial_trigger": True,
            },
        ),
        defaultFactory=get_parent_assigned_group,
    )

    assigned_user = LocalRoleField(
        title=_(u"Assigned user"),
        required=False,
        vocabulary="collective.task.AssignedUsers",  # terms as username, userid, fullname
    )

    due_date = schema.Date(
        title=_(u"Due date"),
        required=False,
        min=datetime.date(1990, 1, 1),
        max=datetime.date(now.year + 1, 12, 31),
    )

    enquirer = LocalRoleField(
        title=_(u"Enquirer"),
        required=False,
        vocabulary="collective.task.Enquirer",
        defaultFactory=get_current_user_id,
    )


class ITaskWithFieldset(ITask):

    """ITask behavior with fieldset."""

    fieldset(
        "task",
        label=_(u"Task"),
        fields=(
            "assigned_group",
            "assigned_user",
            "enquirer",
            "due_date",
        ),
    )

    assigned_group = LocalRoleMasterSelectField(
        title=_(u"Assigned group"),
        required=False,
        vocabulary="plone.principalsource.Groups",
        slave_fields=(
            {
                "name": "ITaskWithFieldset.assigned_user",
                "slaveID": "#form-widgets-ITaskWithFieldset-assigned_user",
                "action": "vocabulary",
                "vocab_method": get_users_vocabulary,
                "control_param": "group",
                "initial_trigger": True,
            },
        ),
    )


alsoProvides(ITask, IFormFieldProvider)
alsoProvides(ITaskWithFieldset, IFormFieldProvider)


class AssignedUserValidator(validator.SimpleFieldValidator):
    def validate(self, value):
        # we go out if assigned user is empty
        if value is None:
            return
        # check if we are editing a task
        if isinstance(self.view, DefaultEditForm) and self.context.portal_type == "task":
            # check if assigned_group is changed and assigned_user is no more in
            if (
                self.context.assigned_group is not None
                and self.context.assigned_user is not None
                and self.request.form["form.widgets.ITask.assigned_group"]
                and self.request.form["form.widgets.ITask.assigned_group"][0] != self.context.assigned_group
            ):
                try:
                    users = api.user.get_users(groupname=self.request.form["form.widgets.ITask.assigned_group"][0])
                except api.exc.GroupNotFoundError:
                    return
                if value not in [mb.getUserName() for mb in users]:
                    raise Invalid(_(u"The assigned user is not in the selected assigned group !"))


validator.WidgetValidatorDiscriminators(AssignedUserValidator, field=ITask["assigned_user"])
