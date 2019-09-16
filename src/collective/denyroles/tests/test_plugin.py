# -*- coding: utf-8 -*-
from collective.denyroles import config
from zope.publisher.browser import TestRequest

import unittest


class TestUser(object):
    def __init__(self, userid, roles=None):
        self.userid = userid
        self._roles = roles or ()

    def getRoles(self):  # noqa P001
        # P001 found "getRoles" consider replacing it with:
        # plone.api.user.get_roles or plone.api.group.get_roles (since plone.api version 1.0)
        return self._roles


class BasePluginTestCase(unittest.TestCase):
    """Base test case class with a few helper methods."""

    def _make_request(self, do_check=False, dont_check=False):
        # Add zero, one or two headers to the request headers.
        environ = {}
        if do_check:
            environ[config.DO_CHECK_ROLES_HEADER] = 1
        if dont_check:
            environ[config.DONT_CHECK_ROLES_HEADER] = 1
        return TestRequest(environ=environ)


class TestPluginUnit(BasePluginTestCase):
    """Test that the plugin works on its own, not yet in Plone."""

    def test_getRolesForPrincipal_member_default(self):
        request = self._make_request()
        plugin = self._make_plugin(request)
        user = TestUser("pipo", roles=["Member"])
        self.assertEqual(plugin.getRolesForPrincipal(user, request), ())

    def test_getRolesForPrincipal_member_do_check(self):
        request = self._make_request(do_check=True)
        plugin = self._make_plugin(request)
        user = TestUser("pipo", roles=["Member"])
        self.assertEqual(plugin.getRolesForPrincipal(user, request), ())

    def test_getRolesForPrincipal_member_dont_check(self):
        request = self._make_request(dont_check=True)
        plugin = self._make_plugin(request)
        user = TestUser("pipo", roles=["Member"])
        self.assertEqual(plugin.getRolesForPrincipal(user, request), ())

    def test_getRolesForPrincipal_member_both(self):
        request = self._make_request(do_check=True, dont_check=True)
        plugin = self._make_plugin(request)
        user = TestUser("pipo", roles=["Member"])
        self.assertEqual(plugin.getRolesForPrincipal(user, request), ())

    def test_getRolesForPrincipal_manager_default(self):
        request = self._make_request()
        plugin = self._make_plugin(request)
        user = TestUser("pipo", roles=["Manager"])
        with self.assertRaises(Forbidden):
            plugin.getRolesForPrincipal(user, request)

    def test_getRolesForPrincipal_manager_do_check(self):
        request = self._make_request(do_check=True)
        plugin = self._make_plugin(request)
        user = TestUser("pipo", roles=["Manager"])
        with self.assertRaises(Forbidden):
            plugin.getRolesForPrincipal(user, request)

    def test_getRolesForPrincipal_manager_dont_check(self):
        request = self._make_request(dont_check=True)
        plugin = self._make_plugin(request)
        user = TestUser("pipo", roles=["Manager"])
        self.assertEqual(plugin.getRolesForPrincipal(user, request), ())

    def test_getRolesForPrincipal_manager_both(self):
        request = self._make_request(do_check=True, dont_check=True)
        plugin = self._make_plugin(request)
        user = TestUser("pipo", roles=["Manager"])
        with self.assertRaises(Forbidden):
            plugin.getRolesForPrincipal(user, request)

    def test_getRolesForPrincipal_editor_do_check(self):
        request = self._make_request(do_check=True)
        plugin = self._make_plugin(request)
        user = TestUser("pipo", roles=["Editor"])
        with self.assertRaises(Forbidden):
            plugin.getRolesForPrincipal(user, request)

    def test_getRolesForPrincipal_editor_and_member_do_check(self):
        request = self._make_request(do_check=True)
        plugin = self._make_plugin(request)
        user = TestUser("pipo", roles=["Member", "Editor"])
        with self.assertRaises(Forbidden):
            plugin.getRolesForPrincipal(user, request)


class UtilsTestCase(BasePluginTestCase):
    def test_must_check(self):
        from collective.denyroles import config
        from collective.denyroles.utils import must_check

        # Default:
        config.DENY_ROLES = None
        self.assertTrue(must_check(self._make_request()))
        self.assertTrue(must_check(self._make_request(do_check=True)))
        self.assertFalse(must_check(self._make_request(dont_check=True)))
        self.assertTrue(must_check(self._make_request(dont_check=True, do_check=True)))

        # Never:
        config.DENY_ROLES = False
        self.assertFalse(must_check(self._make_request()))
        self.assertFalse(must_check(self._make_request(do_check=True)))
        self.assertFalse(must_check(self._make_request(dont_check=True)))
        self.assertFalse(must_check(self._make_request(dont_check=True, do_check=True)))

        # Always:
        config.DENY_ROLES = True
        self.assertTrue(must_check(self._make_request()))
        self.assertTrue(must_check(self._make_request(do_check=True)))
        self.assertTrue(must_check(self._make_request(dont_check=True)))
        self.assertTrue(must_check(self._make_request(dont_check=True, do_check=True)))
