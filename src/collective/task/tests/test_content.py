import datetime

from plone import api

from ecreall.helpers.testing.base import BaseTest

from ..testing import IntegrationTestCase


class TestContentTypes(IntegrationTestCase, BaseTest):
    """Tests content types"""

    def setUp(self):
        super(TestContentTypes, self).setUp()
        portal = api.portal.get()
        folder = portal['folder']
        params = {'type': 'task',
                  'title': u'My task',
                  'responsible': ['bigboss'],
                  'deadline': datetime.datetime(2013, 11, 2, 17, 0),
                  }
        folder.invokeFactory('task', "my-task", **params)
        self.mytask = folder['my-task']

    def test_add_task(self):
        portal = api.portal.get()
        folder = portal['folder']
        self.assertIn('my-task', folder)

    def test_task_fields(self):
        mytask = self.mytask
        self.assertEqual(u'My task', mytask.Title())
        self.assertEqual(datetime.datetime(2013, 11, 2, 17, 0), mytask.deadline)
        self.assertEqual(['bigboss'], mytask.responsible)
