# -*- coding: utf-8 -*-
from collective.task.browser.table import AssignedGroupColumn
from collective.task.browser.table import AssignedUserColumn
from collective.task.browser.table import DueDateColumn
from collective.task.browser.table import EnquirerColumn
from collective.task.browser.table import ReviewStateColumn
from collective.task.browser.table import TasksTable
from collective.task.browser.table import TitleColumn
from collective.task.browser.table import UserColumn
from collective.task.testing import COLLECTIVE_TASK_FUNCTIONAL_TESTING
from datetime import datetime
from plone import api
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME

import unittest2 as unittest


class TestTable(unittest.TestCase):

    layer = COLLECTIVE_TASK_FUNCTIONAL_TESTING

    def setUp(self):
        super(TestTable, self).setUp()
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.task1 = api.content.create(container=self.portal, type='task', id='task1', title='Task1')
        self.task2 = api.content.create(container=self.task1, type='task', id='task2', title='Task2')
        self.task3 = api.content.create(container=self.task1, type='task', id='task3', title='Task3')

    def test_taskstable(self):
        table = TasksTable(self.task1, self.task1.REQUEST)
        table.results = [self.task2, self.task3]
        table.update()
        table.translation_service
        table.wtool
        table.portal_url
        table.values

    def test_UserColumn(self):
        col = UserColumn(self.portal, self.portal.REQUEST, None)
        col.field = 'assigned_user'
        self.assertEqual(col.renderCell(self.task1), '')
        self.task1.assigned_user = TEST_USER_ID
        self.assertEqual(col.renderCell(self.task1), '')

    def test_TitleColumn(self):
        col = TitleColumn(self.portal, self.portal.REQUEST, None)
        self.assertEqual(col.renderCell(self.task1),
                         u'<a href="http://nohost/plone/task1" class="state-created contenttype-task">Task1</a>')

    def test_EnquirerColumn(self):
        col = EnquirerColumn(self.portal, self.portal.REQUEST, None)
        self.task1.enquirer = TEST_USER_ID
        self.assertEqual(col.renderCell(self.task1), '')

    def test_AssignedGroupColumn(self):
        col = AssignedGroupColumn(self.portal, self.portal.REQUEST, None)
        self.task1.assigned_group = None
        self.assertEqual(col.renderCell(self.task1), '')
        self.task1.assigned_group = 'Administrators'
        self.assertEqual(col.renderCell(self.task1), 'Administrators')

    def test_AssignedUserColumn(self):
        col = AssignedUserColumn(self.portal, self.portal.REQUEST, None)
        self.task1.assigned_user = TEST_USER_ID
        self.assertEqual(col.renderCell(self.task1), '')

    def test_DueDateColumn(self):
        col = DueDateColumn(self.portal, self.portal.REQUEST, None)
        self.task1.due_date = None
        self.assertEqual(col.renderCell(self.task1), '')
        self.task1.due_date = datetime(2015, 11, 25, 13, 36, 59)
        self.assertIn(col.renderCell(self.task1), ['Nov 25, 2015', '2015-11-25'])
        col.long_format = True
        self.assertIn(col.renderCell(self.task1), ['Nov 25, 2015 01:36 PM', '2015-11-25 13:36'])

    def test_ReviewStateColumn(self):
        col = ReviewStateColumn(self.portal, self.portal.REQUEST, None)
        self.assertIn(col.renderCell(self.task1), [u'Created', u'created'])
