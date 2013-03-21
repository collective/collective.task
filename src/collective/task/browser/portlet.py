from zope import schema
from zope.interface import implements
from zope.formlib import form

from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from collective.task import _


class ITasksPortlet(IPortletDataProvider):
    """A portlet to display the list of tasks related to the current object"""

    name = schema.TextLine(
            title=_(u"Title"),
            description=_(u"The title of the box."),
            default=u"",
            required=False)


class TasksAssignment(base.Assignment):
    implements(ITasksPortlet)
    title = _(u'Tasks')
    name = u""

    def __init__(self, name=u""):
        self.name = name


class TasksRenderer(base.Renderer):
    def title(self):
        return self.data.name or self.data.title

    def hasName(self):
        return self.data.name

    def update(self):
        pass

    def render(self):
        return self._template()

    def tasks(self):
        portal_catalog = getToolByName(self, 'portal_catalog')
        folder_path = '/'.join(self.context.getPhysicalPath())

        query = {}
        query['path'] = {'query' : folder_path}
        query['portal_type'] = 'task'

        return [x.getObject() for x in portal_catalog.searchResults(query)]

    _template = ViewPageTemplateFile('tasks-portlet.pt')


class TasksAddForm(base.AddForm):
    form_fields = form.Fields(ITasksPortlet)
    label = _(u"Add Tasks Portlet")
    description = _(u"This portlet displays the list of related tasks.")

    def create(self, data):
        return TasksAssignment(name=data.get('name', u""))


class TasksEditForm(base.EditForm):
    form_fields = form.Fields(ITasksPortlet)
    label = _(u"Edit Tasks Portlet")
    description = _(u"This portlet displays the list of related tasks.")
