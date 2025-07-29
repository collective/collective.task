# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""
from collective.task import PLONE_VERSION
from collective.task.testing import COLLECTIVE_TASK_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestInstall(unittest.TestCase):
    """Test installation of collective.task into Plone."""

    layer = COLLECTIVE_TASK_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        if PLONE_VERSION >= "5.1":
            from plone.base.utils import get_installer  # noqa

            self.installer = get_installer(self.portal, self.layer["request"])
            self.ipi = self.installer.is_product_installed
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")  # noqa
            self.ipi = self.installer.isProductInstalled

    def test_product_installed(self):
        """Test if collective.task is installed with portal_quickinstaller."""
        self.assertTrue(self.ipi("collective.task"))

    def test_uninstall(self):
        """Test if collective.task is cleanly uninstalled."""
        if PLONE_VERSION >= "5.1":
            self.installer.uninstall_product("collective.task")
        else:
            self.installer.uninstallProducts(["collective.task"])
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
