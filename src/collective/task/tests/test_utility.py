# -*- coding: utf-8 -*-
from collective.task.behaviors import ITaskContainer
from collective.task.testing import COLLECTIVE_TASK_FUNCTIONAL_TESTING
from collective.task.utility import TaskContainerRelatedSearch
from dexterity.localroles.interfaces import ILocalRolesRelatedSearchUtility
from plone import api
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from zope.component import getUtility
from zope.interface import alsoProvides

import unittest2 as unittest


class TestRelatedSearchUtility(unittest.TestCase):

    layer = COLLECTIVE_TASK_FUNCTIONAL_TESTING

    def setUp(self):
        super(TestRelatedSearchUtility, self).setUp()
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

    def test_get_objects(self):
        task1 = api.content.create(container=self.portal, type='task', id='task1', title='Task1')
        utility = getUtility(ILocalRolesRelatedSearchUtility, 'collective.task.related_taskcontainer')
        self.assertIsInstance(utility, TaskContainerRelatedSearch)
        self.assertEqual(utility.get_objects(task1), [])
        task2 = api.content.create(container=task1, type='task', id='task2', title='Task2')
        self.assertEqual(utility.get_objects(task2), [task1])
        alsoProvides(self.portal, ITaskContainer)
        self.assertListEqual(utility.get_objects(task2), [task1, self.portal])
        setRoles(self.portal, TEST_USER_ID, [])
        self.assertListEqual(utility.get_objects(task2), [task1, self.portal])
