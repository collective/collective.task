# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from collective.task.testing import IntegrationTestCase
from plone import api


class TestInstall(IntegrationTestCase):
    """Test installation of collective.task into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.task is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('collective.task'))

    def test_uninstall(self):
        """Test if collective.task is cleanly uninstalled."""
        self.installer.uninstallProducts(['collective.task'])
        self.assertFalse(self.installer.isProductInstalled('collective.task'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that ICollectiveTaskLayer is registered."""
        from collective.task.interfaces import ICollectiveTaskLayer
        from plone.browserlayer import utils
        self.failUnless(ICollectiveTaskLayer in utils.registered_layers())
