# -*- coding: utf-8 -*-
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer


class CollectiveDenyRolesLayer(PloneSandboxLayer):
    pass


COLLECTIVE_DENYROLES_FIXTURE = CollectiveDenyRolesLayer()


COLLECTIVE_DENYROLES_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_DENYROLES_FIXTURE,), name="CollectiveDenyRolesLayer:IntegrationTesting"
)


COLLECTIVE_DENYROLES_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_DENYROLES_FIXTURE,), name="CollectiveDenyRolesLayer:FunctionalTesting"
)
