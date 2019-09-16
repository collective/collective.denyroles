# -*- coding: utf-8 -*-
# The next line needs plone.app.event[test].  Maybe not for all Plone versions.
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer

import collective.denyroles


class CollectiveDenyRolesLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=collective.denyroles)


COLLECTIVE_DENYROLES_FIXTURE = CollectiveDenyRolesLayer()


COLLECTIVE_DENYROLES_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_DENYROLES_FIXTURE,), name="CollectiveDenyRolesLayer:IntegrationTesting"
)


COLLECTIVE_DENYROLES_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_DENYROLES_FIXTURE,), name="CollectiveDenyRolesLayer:FunctionalTesting"
)
