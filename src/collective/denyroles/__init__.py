# -*- coding: utf-8 -*-
from AccessControl.Permissions import manage_users as ManageUsers
from Products.PluggableAuthService.PluggableAuthService import registerMultiPlugin


def initialize(context):  # pragma: no cover
    """Initializer called when used as a Zope 2 product."""
    from collective.denyroles import plugins

    registerMultiPlugin(plugins.DenyRolesPlugin.meta_type)
    context.registerClass(
        plugins.DenyRolesPlugin,
        permission=ManageUsers,
        constructors=(plugins.add_denyroles_plugin,),
        # icon='www/PluggableAuthService.png',
    )
