# -*- coding: utf-8 -*-
from collective.eeafaceted.batchactions.browser.views import brains_from_uids
from collective.task.browser.batchactions import AssignedGroupBatchActionForm
from collective.task.browser.batchactions import AssignedUserBatchActionForm
from collective.task.testing import COLLECTIVE_TASK_FUNCTIONAL_TESTING
from plone import api
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME

import unittest2 as unittest


class TestBatchActions(unittest.TestCase):

    layer = COLLECTIVE_TASK_FUNCTIONAL_TESTING

    def setUp(self):
        super(TestBatchActions, self).setUp()
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.task1 = api.content.create(container=self.portal, type='task', id='task1', title='Task1',
                                        assigned_group='Site Administrators', enquirer='Reviewers')
        self.task2 = api.content.create(container=self.portal, type='task', id='task2', title='Task2',
                                        assigned_group='Administrators', enquirer='Administrators')
        self.uids = u"{0},{1}".format(self.task1.UID(), self.task2.UID())
        login(self.portal, TEST_USER_NAME)
        setRoles(self.portal, TEST_USER_ID, ['Member'])

    def test_AssignedGroupBatchActionForm_ok(self):
        # User is owner and can modify the tasks
        agbaf = AssignedGroupBatchActionForm(self.portal, self.portal.REQUEST)
        agbaf.brains = brains_from_uids(self.uids)
        agbaf._update()
        self.assertTrue(agbaf.do_apply)  # can modify
        self.assertIn('assigned_group', agbaf.fields)
        fld = agbaf.fields['assigned_group'].field
        self.assertEquals(fld.description, u'')
        self.assertIsNone(fld.vocabulary)
        self.assertEquals(fld.vocabularyName, u'collective.task.AssignedGroups')
        agbaf._apply(**{'assigned_group': 'Reviewers'})
        self.assertEquals(self.task1.assigned_group, 'Reviewers')
        self.assertEquals(self.task2.assigned_group, 'Reviewers')

    def test_AssignedGroupBatchActionForm_not_permitted(self):
        # User cannot modify the tasks
        agbaf = AssignedGroupBatchActionForm(self.portal, self.portal.REQUEST)
        api.group.add_user(groupname='Reviewers', username=TEST_USER_ID)
        self.assertEquals([mb.getId() for mb in agbaf.get_group_users('Administrators')], [])
        self.assertEquals([mb.getId() for mb in agbaf.get_group_users('Reviewers')], ['test_user_1_'])
        api.content.transition(self.task1, 'do_to_assign')
        agbaf.brains = brains_from_uids(self.uids)
        agbaf._update()
        self.assertFalse(agbaf.do_apply)  # cannot modify task1
        self.assertIn('assigned_group', agbaf.fields)
        fld = agbaf.fields['assigned_group'].field
        self.assertEquals(fld.description, u"You can't change this field on selected items. Modify your selection.")
        self.assertIsNone(fld.vocabularyName)
        self.assertEquals(len(fld.vocabulary), 0)

    def test_AssignedGroupBatchActionForm_bad_user(self):
        # User is owner and can modify the tasks but assigned user problem
        agbaf = AssignedGroupBatchActionForm(self.portal, self.portal.REQUEST)
        self.task1.assigned_user = 'test_user_1_'
        self.task1.reindexObject()
        agbaf.brains = brains_from_uids(self.uids)
        agbaf._update()
        self.assertTrue(agbaf.do_apply)
        agbaf._apply(**{'assigned_group': 'Reviewers'})
        # No modification because user 'test_user_1_' is not in Reviewers group
        self.assertEquals(self.task1.assigned_group, 'Site Administrators')
        self.assertEquals(self.task2.assigned_group, 'Administrators')

    def test_AssignedUserBatchActionForm_ok(self):
        # All is rigth
        agbaf = AssignedUserBatchActionForm(self.portal, self.portal.REQUEST)
        api.user.create('x@imio.be', 'officer', '12345')
        api.group.add_user(groupname='Site Administrators', username='officer')
        api.group.add_user(groupname='Administrators', username='officer')
        agbaf.brains = brains_from_uids(self.uids)
        voc = agbaf.get_available_assigneduser_voc()
        self.assertListEqual([term.value for term in voc._terms], ['__none__', 'officer'])
        agbaf._update()
        self.assertTrue(agbaf.do_apply)  # can modify
        self.assertIn('assigned_user', agbaf.fields)
        fld = agbaf.fields['assigned_user'].field
        self.assertEquals(fld.description, u'')
        self.assertIsNone(fld.vocabularyName)
        self.assertEquals(len(fld.vocabulary), 2)
        agbaf._apply(**{'assigned_user': 'officer'})
        self.assertEquals(self.task1.assigned_user, 'officer')
        self.assertEquals(self.task2.assigned_user, 'officer')

    def test_AssignedUserBatchActionForm_no_user(self):
        # No common user
        agbaf = AssignedUserBatchActionForm(self.portal, self.portal.REQUEST)
        api.user.create('x@imio.be', 'officer', '12345')
        api.group.add_user(groupname='Site Administrators', username='officer')
        self.task1.assigned_user = 'test_user_1_'
        self.task1.reindexObject()
        agbaf.brains = brains_from_uids(self.uids)
        voc = agbaf.get_available_assigneduser_voc()
        self.assertListEqual([term.value for term in voc._terms], ['__none__'])
        agbaf._update()
        self.assertTrue(agbaf.do_apply)  # can modify
        self.assertIn('assigned_user', agbaf.fields)
        fld = agbaf.fields['assigned_user'].field
        self.assertEquals(fld.description, u'No common or available assigned group, or no available assigned user. '
                                           u'Modify your selection unless you want to remove assigned user.')
        self.assertIsNone(fld.vocabularyName)
        self.assertEquals(len(fld.vocabulary), 1)
        agbaf._apply(**{'assigned_user': '__none__'})
        self.assertEquals(self.task1.assigned_user, None)
        self.assertEquals(self.task2.assigned_user, None)

    def test_AssignedUserBatchActionForm_not_permitted(self):
        # Cannot modify
        agbaf = AssignedUserBatchActionForm(self.portal, self.portal.REQUEST)
        api.user.create('x@imio.be', 'officer', '12345')
        api.group.add_user(groupname='Site Administrators', username='officer')
        api.group.add_user(groupname='Administrators', username='officer')
        api.group.add_user(groupname='Reviewers', username=TEST_USER_ID)
        api.content.transition(self.task1, 'do_to_assign')
        agbaf.brains = brains_from_uids(self.uids)
        voc = agbaf.get_available_assigneduser_voc()
        self.assertListEqual([term.value for term in voc._terms], ['__none__', 'officer'])
        agbaf._update()
        self.assertFalse(agbaf.do_apply)  # cannot modify
        self.assertIn('assigned_user', agbaf.fields)
        fld = agbaf.fields['assigned_user'].field
        self.assertEquals(fld.description, u"You can't change this field on selected items. Modify your selection.")
        self.assertIsNone(fld.vocabularyName)
        self.assertEquals(len(fld.vocabulary), 0)
