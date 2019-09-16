# -*- coding: utf-8 -*-
# The next line needs plone.app.event[test].  Maybe not for all Plone versions.
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer


class CollectiveDenyRolesLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)


COLLECTIVE_DENYROLES_FIXTURE = CollectiveDenyRolesLayer()


COLLECTIVE_DENYROLES_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_DENYROLES_FIXTURE,), name="CollectiveDenyRolesLayer:IntegrationTesting"
)


COLLECTIVE_DENYROLES_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_DENYROLES_FIXTURE,), name="CollectiveDenyRolesLayer:FunctionalTesting"
)
