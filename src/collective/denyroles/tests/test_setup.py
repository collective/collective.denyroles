# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.denyroles import config
from collective.denyroles.testing import COLLECTIVE_DENYROLES_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFPlone.utils import get_installer

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.denyroles is properly installed."""

    layer = COLLECTIVE_DENYROLES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal)

    def test_product_installed(self):
        """Test if collective.denyroles is installed."""
        self.assertTrue(self.installer.is_product_installed("collective.denyroles"))

    def test_plugin_installed(self):
        from collective.denyroles.config import PLUGIN_ID

        self.assertIn(PLUGIN_ID, self.portal.acl_users.objectIds())

    def test_add_denyroles_plugin(self):
        # We do not use this, but it should not fail either.
        from collective.denyroles.plugins import add_denyroles_plugin

        self.assertIsNone(add_denyroles_plugin())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_DENYROLES_INTEGRATION_TESTING

    def setUp(self):
        # Make sure we can do some stuff in this method without raising Forbidden.
        self._orig_deny_roles = config.DENY_ROLES
        config.DENY_ROLES = False

        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal)
        roles_before = api.user.get_roles(username=TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.assertTrue(self.installer.uninstall_product("collective.denyroles"))
        setRoles(self.portal, TEST_USER_ID, roles_before)
        # Restore the original setting:
        config.DENY_ROLES = self._orig_deny_roles

    def tearDown(self):
        # Restore the original setting, also when test setup fails:
        config.DENY_ROLES = self._orig_deny_roles

    def test_product_uninstalled(self):
        """Test if collective.denyroles is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed("collective.denyroles"))
        self.assertTrue(self.installer.is_product_installable("collective.denyroles"))

    def test_plugin_uninstalled(self):
        from collective.denyroles.config import PLUGIN_ID

        self.assertNotIn(PLUGIN_ID, self.portal.acl_users.objectIds())
