# -*- coding: utf-8 -*-
import unittest
from plone import api
from plone.app.testing import login, TEST_USER_NAME, setRoles, TEST_USER_ID

from ..testing import COLLECTIVE_TASK_FUNCTIONAL_TESTING
from ..interfaces import ITaskMethods


class TestAdapters(unittest.TestCase):

    layer = COLLECTIVE_TASK_FUNCTIONAL_TESTING

    def setUp(self):
        super(TestAdapters, self).setUp()
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.task1 = api.content.create(container=self.portal, type='task', id='task1', title='Task1')
        self.folder = api.content.create(container=self.portal, type='Folder', id='folder', title='Folder')
        self.task2 = api.content.create(container=self.folder, type='task', id='task2', title='Task2')
        self.task3 = api.content.create(container=self.task2, type='task', id='task3', title='Task3')

    def test_get_highest_task_parent(self):
        self.assertEqual(ITaskMethods(self.task1).get_highest_task_parent(), self.portal)
        self.assertEqual(ITaskMethods(self.task1).get_highest_task_parent(task=True), self.task1)
        self.assertEqual(ITaskMethods(self.task2).get_highest_task_parent(), self.folder)
        self.assertEqual(ITaskMethods(self.task2).get_highest_task_parent(task=True), self.task2)
        self.assertEqual(ITaskMethods(self.task3).get_highest_task_parent(), self.folder)
        self.assertEqual(ITaskMethods(self.task3).get_highest_task_parent(task=True), self.task2)
