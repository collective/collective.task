# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""
from collective.task.testing import COLLECTIVE_TASK_INTEGRATION_TESTING  # noqa
from plone.base.utils import get_installer

import unittest


class TestInstall(unittest.TestCase):
    """Test installation of collective.task into Plone."""

    layer = COLLECTIVE_TASK_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])
        self.ipi = self.installer.is_product_installed

    def test_product_installed(self):
        """Test if collective.task is installed."""
        self.assertTrue(self.ipi("collective.task"))

    def test_uninstall(self):
        """Test if collective.task is cleanly uninstalled."""
        self.installer.uninstall_product("collective.task")
        self.assertFalse(self.ipi("collective.task"))

    def test_uninstall_1(self):
        """Test if collective.task is cleanly uninstalled."""
        self.portal.portal_setup.runAllImportStepsFromProfile("profile-collective.task:uninstall_1.0")

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that ICollectiveTaskLayer is registered."""
        from collective.task.interfaces import ICollectiveTaskLayer
        from plone.browserlayer import utils

        self.assertIn(ICollectiveTaskLayer, utils.registered_layers())
