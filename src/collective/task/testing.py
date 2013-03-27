# -*- coding: utf-8 -*-
"""Base module for unittesting."""

from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import login
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.testing import z2

import unittest2 as unittest

from ecreall.helpers.testing import member as memberhelpers

import collective.task


USERDEFS = [{'user': 'manager', 'roles': ('Member', 'Manager' ), 'groups': ()},
            {'user': 'bigboss', 'roles': ('Member', ), 'groups': ()},
            {'user': 'miniboss', 'roles': ('Member', ), 'groups': ()},
            {'user': 'grunt', 'roles': ('Member', ), 'groups': ()},
            ]

class CollectiveTaskLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        # Load ZCML
        self.loadZCML(package=collective.task,
                      name='testing.zcml')
        z2.installProduct(app, 'collective.task')

    def setUpPloneSite(self, portal):
        """Set up Plone."""
        # Install into Plone site using portal_setup
        applyProfile(portal, 'collective.task:default')

        # create users
        memberhelpers.createMembers(portal, USERDEFS)

        # Login and create some test content
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        portal.invokeFactory('Folder', 'folder')

        # Commit so that the test browser sees these objects
        portal.portal_catalog.clearFindAndRebuild()
        import transaction
        transaction.commit()

    def tearDownZope(self, app):
        """Tear down Zope."""
        z2.uninstallProduct(app, 'collective.task')


FIXTURE = CollectiveTaskLayer(
    name="FIXTURE"
    )

INTEGRATION = IntegrationTesting(
    bases=(FIXTURE,),
    name="INTEGRATION"
    )

FUNCTIONAL = FunctionalTesting(
    bases=(FIXTURE,),
    name="FUNCTIONAL"
    )


class IntegrationTestCase(unittest.TestCase):
    """Base class for integration tests."""

    layer = INTEGRATION

    def setUp(self):
        super(IntegrationTestCase, self).setUp()
        self.portal = self.layer['portal']


class FunctionalTestCase(unittest.TestCase):
    """Base class for functional tests."""

    layer = FUNCTIONAL