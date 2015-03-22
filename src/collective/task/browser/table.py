# -*- coding: utf-8 -*-
"""Define tables and columns."""
import datetime

from zope.cachedescriptors.property import CachedProperty
from zope.i18n import translate

from plone import api

from z3c.table.column import Column, LinkColumn
from z3c.table.table import Table

from collective.task import _, PMF


class TasksTable(Table):

    """Table that displays tasks info."""

    cssClassEven = u'even'
    cssClassOdd = u'odd'
    cssClasses = {'table': 'listing taskContainerListing'}

    batchSize = 20
    startBatchingAt = 30
    results = []

    @CachedProperty
    def translation_service(self):
        return api.portal.get_tool('translation_service')

    @CachedProperty
    def wtool(self):
        return api.portal.get_tool('portal_workflow')

    @CachedProperty
    def portal_url(self):
        return api.portal.get().absolute_url()

    def format_date(self, date, long_format=None, time_only=None):
        if date is None:
            return u""

        # If date is a datetime object, isinstance(date, datetime.date)
        # returns True, so we use type here.
        if type(date) == datetime.date:
            date = date.strftime('%Y/%m/%d')
        elif type(date) == datetime.datetime:
            date = date.strftime('%Y/%m/%d %H:%M')

        return self.translation_service.ulocalized_time(
            date,
            long_format=long_format,
            time_only=time_only,
            context=self.context,
            domain='plonelocales',
            request=self.request) or ''

    @CachedProperty
    def values(self):
        return self.results


class UserColumn(Column):

    """Base user column."""

    field = NotImplemented

    def renderCell(self, value):
        username = getattr(value, self.field, '')
        if username:
            member = api.user.get(username)
            return member.getUser().getProperty('fullname').decode('utf-8')

        return ""


class TitleColumn(LinkColumn):

    """Column that displays title."""

    header = PMF("Title")
    weight = 10

    def getLinkCSS(self, item):
        return 'class=state-%s contenttype-%s' % (api.content.get_state(obj=item),
                                                  item.portal_type)

    def getLinkContent(self, item):
        return item.title


class EnquirerColumn(UserColumn):

    """Column that displays enquirer."""

    header = _("Enquirer")
    weight = 20
    field = 'enquirer'


class AssignedGroupColumn(Column):

    """Column that displays assigned group."""

    header = _("Assigned group")
    weight = 30

    def renderCell(self, value):
        if value.assigned_group:
            group = api.group.get(value.assigned_group).getGroup()
            return group.getProperty('title').decode('utf-8')

        return ""


class AssignedUserColumn(UserColumn):

    """Column that displays assigned user."""

    header = _("Assigned user")
    weight = 40
    field = 'assigned_user'


class DueDateColumn(Column):

    """Column that displays due date."""

    header = _("Due date")
    weight = 50

    def renderCell(self, value):
        if value.due_date:
            return self.table.format_date(value.due_date)

        return ""


class ReviewStateColumn(Column):

    """Column that displays value's review state."""

    header = PMF("Review state")
    weight = 60

    def renderCell(self, value):
        state = api.content.get_state(value)
        if state:
            wtool = api.portal.get_tool('portal_workflow')
            state_title = wtool.getTitleForStateOnType(state, value.portal_type)
            return translate(PMF(state_title), context=self.request)

        return ''
