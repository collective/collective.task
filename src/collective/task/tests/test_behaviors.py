# -*- coding: utf-8 -*-
import datetime
import unittest2 as unittest
from plone import api
from plone.app.testing import login, TEST_USER_NAME, setRoles, TEST_USER_ID

from ..behaviors import get_users_vocabulary, get_parent_assigned_group, get_current_user_id
from ..testing import COLLECTIVE_TASK_FUNCTIONAL_TESTING


class TestBehaviors(unittest.TestCase):

    layer = COLLECTIVE_TASK_FUNCTIONAL_TESTING

    def setUp(self):
        super(TestBehaviors, self).setUp()
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        api.group.add_user(groupname='Reviewers', username=TEST_USER_ID)
        self.task1 = api.content.create(container=self.portal, type='task', id='task1', title='Task1',
                                        assigned_group='Reviewers', due_date=datetime.date(2015, 11, 16))

    def test_get_users_vocabulary(self):
        self.assertEqual([v.value for v in get_users_vocabulary('NotAGroup')], [])
        self.assertEqual([v.value for v in get_users_vocabulary('Reviewers')], ['test-user'])

    def test_get_parent_assigned_group(self):
        # Not in an add form
        self.assertEqual(get_parent_assigned_group(self.task1), None)
        # In an add form
        self.task1.REQUEST['PATH_INFO'] = 'http://nohost/plone/++add++task'
        self.assertEqual(get_parent_assigned_group(self.task1), 'Reviewers')
        self.assertEqual(get_parent_assigned_group(self.portal), None)

    def test_get_current_user_id(self):
        self.assertEqual(get_current_user_id(None), 'test_user_1_')
