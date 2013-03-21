from zope.interface import Interface
from five import grok

from Products.CMFCore.utils import getToolByName
from plone.app.layout.viewlets.interfaces import IBelowContentBody

# The viewlets in this file are rendered on every content item type
grok.context(Interface)

# Use templates directory to search for templates.
grok.templatedir('templates')

class RelatedTasksSnippet(grok.Viewlet):
    """A viewlet to display the list of tasks related to the current object"""

    grok.viewletmanager(IBelowContentBody)
    grok.template('related-tasks')

    def available(self):
        # only display the viewlet if current object has an associated task
        return [x for x in self.context.contentValues() if x.portal_type == 'task']

    def tasks(self):
        portal_catalog = getToolByName(self, 'portal_catalog')
        folder_path = '/'.join(self.context.getPhysicalPath())

        query = {}
        query['path'] = {'query' : folder_path}
        query['portal_type'] = 'task'

        return [x.getObject() for x in portal_catalog.searchResults(query)]
