import datetime

from plone import api

from ecreall.helpers.testing.base import BaseTest

from ..testing import IntegrationTestCase


class TestContentTypes(IntegrationTestCase, BaseTest):
    """Tests content types"""

    def setUp(self):
        super(TestContentTypes, self).setUp()
        portal = api.portal.get()
        self.folder = portal['folder']

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
                  'responsible': ['bigboss'],
                  'deadline': datetime.datetime(2013, 11, 2, 17, 0),
                  }
        folder.invokeFactory('task', "my-task", **params)
        mytask = folder['my-task']
        self.assertEqual(u'My task', mytask.Title())
        self.assertEqual(u'This is a huge task', mytask.note)
        self.assertEqual(datetime.datetime(2013, 11, 2, 17, 0), mytask.deadline)
        self.assertEqual(['bigboss'], mytask.responsible)
