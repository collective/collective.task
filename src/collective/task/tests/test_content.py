import datetime

from z3c.relationfield.relation import RelationValue
from zope.component import getUtility
from zope.intid.interfaces import IIntIds

from plone import api

from ecreall.helpers.testing.base import BaseTest

from ..testing import IntegrationTestCase


class TestContentTypes(IntegrationTestCase, BaseTest):
    """Tests content types"""

    def setUp(self):
        super(TestContentTypes, self).setUp()
        portal = api.portal.get()
        self.folder = portal['folder']
        self.document = portal['document']
        intids = getUtility(IIntIds)
        self.doc_intid = intids.getId(self.document)

    def test_add_task(self):
        folder = self.folder
        params = {'title': u'My task',
                  'responsible': ['bigboss'],
                  }
        folder.invokeFactory('task', "my-task", **params)
        self.assertIn('my-task', folder)

    def test_task_fields(self):
        folder = self.folder
        params = {'title': u'My task',
                  'note': u"This is a huge task",
                  'responsible': [u'bigboss'],
                  'deadline': datetime.datetime(2013, 11, 2, 17, 0),
                  }
        folder.invokeFactory('task', "my-task", **params)
        mytask = folder['my-task']
        self.assertEqual(u'My task', mytask.Title())
        self.assertEqual(u'This is a huge task', mytask.note)
        self.assertEqual(datetime.datetime(2013, 11, 2, 17, 0), mytask.deadline)
        self.assertEqual(['bigboss'], mytask.responsible)

    def test_add_information(self):
        portal = api.portal.get()
        folder = portal['folder']
        info = api.content.create(folder, type="information",
                                  id="my-info", title="My information",
                                  responsible=[u'bigboss'])
        self.assertIn('my-info', folder)
        self.assertNotIn('deadline', info.__dict__)

    def test_add_opinion(self):
        folder = self.folder
        info = api.content.create(folder, type="opinion",
                                  id="my-opinion", title="My opinion",
                                  responsible=[u'bigboss'],
                                  target=RelationValue(self.doc_intid))
        self.assertIn('my-opinion', folder)

    def test_add_validation(self):
        folder = self.folder
        info = api.content.create(folder, type="validation",
                                  id="my-validation", title="My validation",
                                  responsible=[u'bigboss'],
                                  target=RelationValue(self.doc_intid))
        self.assertIn('my-validation', folder)
