# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from collective.denyroles import config
from collective.denyroles.utils import must_check
from Globals import InitializeClass
from Products.PluggableAuthService.interfaces import plugins
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.utils import classImplements
from ZPublisher import Forbidden

import logging


logger = logging.getLogger("collective.denyroles")


class DenyRolesPlugin(BasePlugin):
    """PAS Plugin which denies access to users with some global roles.

    IRolesPlugin: Determine the (global) roles which a user has.

    Here we want to check what global roles a user already has,
    and deny access for at least Managers.
    """

    meta_type = "DenyRoles Plugin"
    security = ClassSecurityInfo()

    def getRolesForPrincipal(self, principal, request=None):
        """ principal -> ( role_1, ... role_N )

        o Return a sequence of role names which the principal has.

        o May assign roles based on values in the REQUEST object, if present.
        """
        if not must_check(request):
            # Nothing to do.  Return an empty sequence.
            return ()

        # Get the user roles as determined until now by other plugins.
        # code-analysis wants us to use plone.api:
        # P001 found "getRoles" consider replacing it with:
        # plone.api.user.get_roles or plone.api.group.get_roles (since plone.api version 1.0)
        # But that does not seem the right approach for a plugin, so we ignore it.
        principal_roles = principal.getRoles()  # noqa P001
        for role in config.DENIED_ROLES:
            if role in principal_roles:
                raise Forbidden("Role {0} is not allowed here.".format(role))
        return ()


InitializeClass(DenyRolesPlugin)
classImplements(DenyRolesPlugin, plugins.IRolesPlugin)


def add_denyroles_plugin():
    # Form for manually adding our plugin.
    # But we do this in setuphandlers.py always.
    pass
