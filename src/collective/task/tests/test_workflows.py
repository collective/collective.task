# -*- coding: utf8 -*-
import datetime

from zope.component import getMultiAdapter

from plone import api

from ecreall.helpers.testing.workflow import BaseWorkflowTest

from ..testing import IntegrationTestCase
from ..testing import USERDEFS


TASK_PERMISSIONS = {}

WORKFLOW_TRACK = [('', 'todo'),
                  ('take-responsibility', 'in-progress'),
                  ('mark-as-done', 'done')]

WORKFLOW_TRACK2 = [('', 'todo'),
                   ('ask-for-refusal', 'refusal-requested'),
                   ('refuse-refusal', 'todo'),
                   ('ask-for-refusal', 'refusal-requested'),
                   ('accept-refusal', 'abandoned'),
                   ]

# scénario 3 : attribution à user2, ask for refusal, refus accepté, tâche 1 à todo
# scénario 4 : attribution à user2, fait, tâche 1 à fait
# scénario 5 : ask for refusal à partir de in-progress ???


class TestSecurity(IntegrationTestCase, BaseWorkflowTest):
    """Tests collective.task workflows"""

    def setUp(self):
        super(TestSecurity, self).setUp()

    def FIXME_test_permissions(self):
        self.login('manager')
        portal = api.portal.get()
        folder = portal['folder']
        params = {'type': 'task',
                  'title': u'Main task',
                  'responsible': ['bigboss'],
                  'deadline': datetime.date(2013, 11, 2),
                  }
        folder.invokeFactory('task', "my-task", **params)
        main_task = folder['my-task']

        # user1 attribute task to user2
        #request = ""
        #view = getMultiAdapter((main_task, request), name='attribute_task')

        self.login('bigboss')
        workflow = self.portal.portal_workflow
        workflow.doActionFor(main_task, "attribute")
        #api.content.transition(obj=main_task, transition="attribute")
        # ?????

        #"%s/content_status_modify?workflow_action=attribute" % (container_url, workflow_action)
#
#        for (transition, state) in WORKFLOW_TRACK:
#            if transition:
#                workflow.doActionFor(myissue, transition)
#            if state:
#                self.assertHasState(myissue, state)
#                self.assertCheckPermissions(myissue, ISSUE_PERMISSIONS[state],
#                                            USERDEFS, stateid=state)
    def test_nothing(self):
        self.assertTrue(True)
