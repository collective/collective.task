# -*- coding: utf-8 -*-
from collective.task.browser.viewlets import TaskParentViewlet
from collective.task.testing import COLLECTIVE_TASK_FUNCTIONAL_TESTING
from plone import api
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME

import unittest


class TestTaskParentViewlet(unittest.TestCase):

    layer = COLLECTIVE_TASK_FUNCTIONAL_TESTING

    def setUp(self):
        super(TestTaskParentViewlet, self).setUp()
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.task1 = api.content.create(container=self.portal, type='task', id='task1', title='Task1')
        self.folder = api.content.create(container=self.portal, type='Folder', id='folder', title='Folder')
        self.task2 = api.content.create(container=self.folder, type='task', id='task2', title='Task2')
        self.task3 = api.content.create(container=self.task2, type='task', id='task3', title='Task3')

    def test_viewlet_rendering(self):
        viewlet = TaskParentViewlet(self.task3, self.task3.REQUEST, None)
        output = viewlet.context()
        self.assertIn('<span>Highest task</span>:&nbsp;\n        <a href="http://nohost/plone/folder/task2"',
                      output)
        self.assertIn('<span>Above tasks</span>:&nbsp;\n        <a href="http://nohost/plone/folder"',
                      output)
        viewlet = TaskParentViewlet(self.task1, self.task1.REQUEST, None)
        output = viewlet.context()
        self.assertNotIn('<span>Highest task</span>:&nbsp;\n        <a href="http://nohost/plone/folder/task1"',
                         output)
        self.assertIn('<span>Above tasks</span>:&nbsp;\n        <a href="http://nohost/plone"',
                      output)
