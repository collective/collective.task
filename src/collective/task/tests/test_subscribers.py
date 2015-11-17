# -*- coding: utf-8 -*-
import unittest2 as unittest
from plone import api
from plone.app.testing import login, TEST_USER_NAME, setRoles, TEST_USER_ID

from Products.CMFPlone.utils import base_hasattr
from ..testing import COLLECTIVE_TASK_FUNCTIONAL_TESTING


class TestSubscribers(unittest.TestCase):

    layer = COLLECTIVE_TASK_FUNCTIONAL_TESTING

    def setUp(self):
        super(TestSubscribers, self).setUp()
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.task1 = api.content.create(container=self.portal, type='task', id='task1', title='Task1')

    def test_afterTransitionITaskSubscriber(self):
        # assigned_user is None
        self.assertEqual(self.task1.assigned_user, None)
        api.content.transition(obj=self.task1, transition='do_to_assign')
        self.assertTrue(base_hasattr(self.task1, 'auto_to_do_flag'))
        self.assertFalse(self.task1.auto_to_do_flag)
        self.assertEqual(api.content.get_state(obj=self.task1), 'to_assign')
        api.content.transition(obj=self.task1, transition='back_in_created')
        # assigned_user is set
        self.task1.assigned_user = TEST_USER_ID
        api.content.transition(obj=self.task1, transition='do_to_assign')
        self.assertTrue(self.task1.auto_to_do_flag)
        self.assertEqual(api.content.get_state(obj=self.task1), 'to_do')
        # back in to assign
        api.content.transition(obj=self.task1, transition='back_in_to_assign')
        self.assertFalse(self.task1.auto_to_do_flag)
        self.assertEqual(api.content.get_state(obj=self.task1), 'to_assign')
