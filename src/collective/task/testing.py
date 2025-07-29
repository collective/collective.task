# -*- coding: utf-8 -*-
"""Base module for unittesting."""

from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2
from zope.configuration import xmlconfig

import collective.task


class CollectiveTaskLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        xmlconfig.file("testing.zcml", collective.task, context=configurationContext)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "collective.task:default")


COLLECTIVE_TASK_FIXTURE = CollectiveTaskLayer()


COLLECTIVE_TASK_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_TASK_FIXTURE,), name="CollectiveTaskLayer:IntegrationTesting"
)


COLLECTIVE_TASK_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_TASK_FIXTURE,), name="CollectiveTaskLayer:FunctionalTesting"
)


COLLECTIVE_TASK_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_TASK_FIXTURE, REMOTE_LIBRARY_BUNDLE_FIXTURE, z2.ZSERVER_FIXTURE),
    name="CollectiveTaskLayer:AcceptanceTesting",
)
