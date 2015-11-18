# -*- coding: utf-8 -*-
import unittest2 as unittest
from plone import api
from plone.app.testing import login, TEST_USER_NAME, setRoles, TEST_USER_ID

from ..browser.table import TasksTable, UserColumn
from ..testing import COLLECTIVE_TASK_FUNCTIONAL_TESTING


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
