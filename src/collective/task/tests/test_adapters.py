# -*- coding: utf-8 -*-
import unittest
from plone import api
from plone.app.testing import login, TEST_USER_NAME, setRoles, TEST_USER_ID

from ..adapters import TaskContentAdapter
from ..testing import COLLECTIVE_TASK_FUNCTIONAL_TESTING
from ..interfaces import ITaskMethods


class TestAdapters(unittest.TestCase):

    layer = COLLECTIVE_TASK_FUNCTIONAL_TESTING

    def setUp(self):
        super(TestAdapters, self).setUp()
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.g1 = api.group.create(groupname='g1', title='Group1').id
        self.task1 = api.content.create(container=self.portal, type='task', id='task1', title='Task1',
                                        assigned_group='Administrators')
        self.folder = api.content.create(container=self.portal, type='Folder', id='folder', title='Folder')
        self.task2 = api.content.create(container=self.folder, type='task', id='task2', title='Task2',
                                        assigned_group='Administrators')
        self.task3 = api.content.create(container=self.task2, type='task', id='task3', title='Task3',
                                        assigned_group='Reviewers')
        self.task4 = api.content.create(container=self.task3, type='task', id='task4', title='Task4',
                                        assigned_group='Site Administrators')
        self.task5 = api.content.create(container=self.task4, type='task', id='task5', title='Task5')

    def test_get_highest_task_parent(self):
        self.assertEqual(ITaskMethods(self.task1).get_highest_task_parent(), self.portal)
        self.assertEqual(ITaskMethods(self.task1).get_highest_task_parent(task=True), self.task1)
        self.assertEqual(ITaskMethods(self.task2).get_highest_task_parent(), self.folder)
        self.assertEqual(ITaskMethods(self.task2).get_highest_task_parent(task=True), self.task2)
        self.assertEqual(ITaskMethods(self.task3).get_highest_task_parent(), self.folder)
        self.assertEqual(ITaskMethods(self.task3).get_highest_task_parent(task=True), self.task2)

    def test_get_parents_assigned_groups(self):
        adapted = TaskContentAdapter(self.task5)
        # infos are None
        self.task4.parents_assigned_groups = None
        self.task4.assigned_group = None
        self.assertListEqual(adapted.get_parents_assigned_groups(), [])
        # one of infos is None
        self.task4.parents_assigned_groups = ['Administrators', 'Reviewers']
        self.task4.assigned_group = None
        self.assertListEqual(adapted.get_parents_assigned_groups(), ['Administrators', 'Reviewers'])
        self.task4.parents_assigned_groups = None
        self.task4.assigned_group = 'Site Administrators'
        self.assertListEqual(adapted.get_parents_assigned_groups(), ['Site Administrators'])
        # an item is the same
        self.task4.parents_assigned_groups = ['Administrators', 'Reviewers']
        self.task4.assigned_group = 'Administrators'
        self.assertListEqual(adapted.get_parents_assigned_groups(), ['Administrators', 'Reviewers'])
        # full infos
        self.task4.parents_assigned_groups = ['Administrators', 'Reviewers']
        self.task4.assigned_group = 'Site Administrators'
        self.assertListEqual(adapted.get_parents_assigned_groups(),
                             ['Administrators', 'Reviewers', 'Site Administrators'])

    def test_set_all_parents_value(self):
        self.assertEqual(self.task1.parents_assigned_groups, None)
        self.assertEqual(self.task2.parents_assigned_groups, None)
        self.assertEqual(self.task3.parents_assigned_groups, ['Administrators'])
        self.assertListEqual(self.task4.parents_assigned_groups, ['Administrators', 'Reviewers'])
        self.assertListEqual(self.task5.parents_assigned_groups, ['Administrators', 'Reviewers', 'Site Administrators'])
        self.task2.assigned_group = self.g1
        adapted = TaskContentAdapter(self.task5)
        adapted.set_all_parents_value('parents_assigned_groups', 'get_parents_assigned_groups')
        self.assertEqual(self.task3.parents_assigned_groups, [self.g1])
        self.assertListEqual(self.task4.parents_assigned_groups, [self.g1, 'Reviewers'])
        self.assertListEqual(self.task5.parents_assigned_groups, ['Administrators', 'Reviewers', 'Site Administrators'])
        adapted.set_parents_value('parents_assigned_groups', adapted.get_parents_assigned_groups(), modified=False)
        self.assertListEqual(self.task5.parents_assigned_groups, [self.g1, 'Reviewers', 'Site Administrators'])
