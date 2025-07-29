# -*- coding: utf-8 -*-
"""Batch actions views."""

from collective.task import _
from collective.task.adapters import EMPTY_STRING
from collective.task.behaviors import ITask
from operator import methodcaller
from plone import api
from z3c.form.field import Fields
from z3c.form.form import Form
from zope import schema
from zope.lifecycleevent import Attributes
from zope.lifecycleevent import modified
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


try:
    from plone.base.utils import safe_text
except ImportError:
    from Products.CMFPlone.utils import safe_unicode as safe_text


try:
    from collective.eeafaceted.batchactions.browser.views import BaseBatchActionForm as bbaf

    baf_base = bbaf
    from collective.eeafaceted.batchactions.interfaces import IBatchActionsMarker
    from collective.eeafaceted.batchactions.utils import cannot_modify_field_msg
    from collective.eeafaceted.batchactions.utils import is_permitted

    class ITasksBatchActionsMarker(IBatchActionsMarker):
        """Marker interface for tasks batch actions context."""

    from collective.eeafaceted.batchactions import _ as _ceba

    _ceb = _ceba

except ImportError:
    baf_base = Form
    _ceb = _


class AssignedGroupBatchActionForm(baf_base):
    """
    Batch action that can be used with collective.eeafaceted.batchactions.
    Base class for imio.dms.mail and imio.project.pst.
    """

    label = _ceb(u"Batch assigned group change")
    weight = 20

    def get_group_users(self, assigned_group):
        return api.user.get_users(groupname=assigned_group)

    def _update(self):
        self.do_apply = is_permitted(self.brains)
        self.fields += Fields(
            schema.Choice(
                __name__="assigned_group",
                title=_(u"Assigned group"),
                description=(not self.do_apply and cannot_modify_field_msg or u""),
                required=(self.do_apply),
                vocabulary=self.do_apply and u"collective.task.AssignedGroups" or SimpleVocabulary([]),
            )
        )

    def _apply(self, **data):
        if data["assigned_group"]:
            for brain in self.brains:
                # check if assigned_group is changed and assigned_user is no more in
                if (
                    brain.assigned_group is not None
                    and brain.assigned_user != EMPTY_STRING
                    and data["assigned_group"] != brain.assigned_group
                    and brain.assigned_user
                    not in [mb.getUserName() for mb in self.get_group_users(data["assigned_group"])]
                ):
                    api.portal.show_message(
                        _ceb(
                            u"An assigned user is not in this new assigned group. " u'Task "${task}" !',
                            mapping={"task": safe_text(brain.getURL())},
                        ),
                        self.request,
                        "error",
                    )
                    break
            else:  # here if no break !
                for brain in self.brains:
                    obj = brain.getObject()
                    obj.assigned_group = data["assigned_group"]
                    modified(obj, Attributes(ITask, "ITask.assigned_group"))


class AssignedUserBatchActionForm(baf_base):
    """
    Batch action that can be used with collective.eeafaceted.batchactions.
    Base class for imio.dms.mail and imio.project.pst.
    """

    label = _ceb(u"Batch assigned user change")
    master = "assigned_group"  # attribute name containing group
    err_msg = _ceb(
        u"No common or available assigned group, or no available assigned user. "
        u"Modify your selection unless you want to remove assigned user."
    )
    weight = 30

    def get_group_users(self, assigned_group):
        return api.user.get_users(groupname=assigned_group)

    def get_available_assigneduser_voc(self):
        """Returns available assigned users common for all brains."""
        terms = [SimpleTerm(value="__none__", token="no_value", title=_ceb("Set to no value"))]
        user_ids = None
        for brain in self.brains:
            if not getattr(brain, self.master):
                return SimpleVocabulary([])
            if user_ids is None:
                user_ids = {u.getId() for u in self.get_group_users(getattr(brain, self.master))}
            else:
                user_ids &= {u.getId() for u in self.get_group_users(getattr(brain, self.master))}
        if user_ids:
            members = [api.user.get(userid) for userid in user_ids]
            for member in sorted(members, key=methodcaller("getUserName")):
                terms.append(
                    SimpleTerm(
                        value=member.getUserName(),  # login
                        token=member.getId(),  # id
                        title=member.getUser().getProperty("fullname") or member.getUserName(),
                    )
                )  # title
        return SimpleVocabulary(terms)

    def _update(self):
        self.voc = self.get_available_assigneduser_voc()
        self.do_apply = is_permitted(self.brains)
        self.fields += Fields(
            schema.Choice(
                __name__="assigned_user",
                title=_(u"Assigned user"),
                vocabulary=self.do_apply and self.voc or SimpleVocabulary([]),
                description=(
                    (len(self.voc) <= 1 and self.err_msg) or (not self.do_apply and cannot_modify_field_msg) or u""
                ),
                required=self.do_apply,
            )
        )

    def _apply(self, **data):
        if data["assigned_user"]:
            if data["assigned_user"] == "__none__":
                data["assigned_user"] = None
            for brain in self.brains:
                obj = brain.getObject()
                obj.assigned_user = data["assigned_user"]
                modified(obj, Attributes(ITask, "ITask.assigned_user"))
