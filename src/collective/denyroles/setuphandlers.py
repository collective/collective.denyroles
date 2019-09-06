# -*- coding: utf-8 -*-
from collective.denyroles.config import PLUGIN_ID
from collective.denyroles.utils import must_check
from plone import api
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer
from ZPublisher import Forbidden

import logging


logger = logging.getLogger("collective.denyroles")


@implementer(INonInstallable)
class HiddenProfiles(object):
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return ["collective.denyroles:uninstall"]


def pre_install(context):
    """Pre install script.

    Check that we are not about to lock ourselves out.
    """
    if must_check(context.REQUEST):
        raise Forbidden(
            "Refusing to activate collective.denyroles. "
            "This would lock the current user out. "
            "See https://github.com/collective/collective.denyroles"
        )


def post_install(context):
    """Post install script.

    Setup our denyroles plugin.
    """
    pas = api.portal.get_tool("acl_users")
    ID = PLUGIN_ID

    # Create plugin if it does not exist.
    if ID not in pas.objectIds():
        from collective.denyroles.plugins import DenyRolesPlugin

        plugin = DenyRolesPlugin(title="Deny Roles plugin")
        plugin.id = ID
        pas._setObject(ID, plugin)
        logger.info("Created %s in acl_users.", ID)
    plugin = getattr(pas, ID)

    # Activate all supported interfaces for this plugin.
    activate = []
    plugins = pas.plugins
    for info in plugins.listPluginTypeInfo():
        interface = info["interface"]
        interface_name = info["id"]
        if plugin.testImplements(interface):
            activate.append(interface_name)
            logger.info("Activating interface %s for plugin %s", interface_name, info["title"])

    plugin.manage_activateInterfaces(activate)
    logger.info("Plugins activated.")

    # Order the IRolesPlugin plugins to make sure our plugin is at the bottom.
    for info in plugins.listPluginTypeInfo():
        interface_name = info["id"]
        if interface_name == "IRolesPlugin":
            iface = plugins._getInterfaceFromName(interface_name)
            for _obj in plugins.listPlugins(iface):
                plugins.movePluginsDown(iface, [ID])
            logger.info("Moved %s to bottom of %s.", ID, interface_name)


def uninstall(context):
    """Uninstall script

    Remove our denyroles plugin.
    """
    pas = api.portal.get_tool("acl_users")
    ID = PLUGIN_ID
    if ID in pas.objectIds():
        pas._delObject(ID)
        logger.info("Removed %s from acl_users.", ID)
