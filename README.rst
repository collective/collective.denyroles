.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi. It is a comment.

=============
collective.denyroles
=============

This is a PAS (``PluggableAuthenticationService``) plugin for Plone.
It denies access to Plone Sites for users with roles like Manager or Editor.


Features
--------

- A PAS roles plugin that checks the roles determined up to this point, and forbids access when some roles are found.
- Configuration via environment variables or request headers to see if the check should be done.
- An installer that installs the plugin into ``acl_users``.
- An uninstaller to remove the plugin.


Use case
--------

You have a Plone Site on two domains:

- edit.example.local is for editing.
  Users with the Editor or Manager role login here to edit and manage the site.
  This is a local domain that can only be reached within your local network or a VPN.

- www.example.org is for anonymous users and maybe also for standard Members without extra roles.
  This domain is protected by a special firewall to prevent common web attacks like
  dubious form submissions, request flooding, spammers, cross site scripting attacks, etcetera.

Problems:

- Editors sometimes login to the public domain,
  and get errors during editing because the firewall is too protective.

- The system administrator complains that he has setup a special domain for editing and managing,
  so that no changes can come in from the public site,
  and yet unexpectedly the editors can login and make changes via the public site anyway.

This add-on gives you options to prevent users with some global roles from accesing the (public) site.


Installation
------------

Install collective.denyroles by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.denyroles


and then running ``bin/buildout``.

Install the product in the Add-ons control panel in Plone.

You may need some more configuration in your buildout config.
See the next section.


Configuration
-------------

The roles that are denied access, can be seen in ``src/collective.denyroles/config.py``.
We might make this configurable at some point.

There are two ways to configure whether the roles should be checked or not:
via environment variables or via request headers.


Environment variables
~~~~~~~~~~~~~~~~~~~~~

You can set an environment variable to always deny the roles::

    export DENY_ROLES=1

Set this either to 1 for yes, and 0 (or anything else) for no.

The OS environment can be different when you manually start your Plone instance or start it in a cronjob.
So it is better to set this in your Plone ``buildout.cfg``::

    [instance]
    recipe = plone.recipe.zope2instance
    environment-vars =
        DENY_ROLES 1

Run the buildout and it will be set in the Plone config,
in this case in ``parts/instance/etc/zope.conf``.

The environment variable is useful when the roles should be checked for *all* traffic to this Plone instance.
If you have a ZEO setup with one zeoclient that gets all traffic from editors, and another for anonymous visitors, you can do this:

- zeoclient for editors: ``DENY_ROLES = 0``
- zeoclient for anonymous: ``DENY_ROLES = 1``

Now editors can edit normally in their edit environment.
And when they accidentally login on the anonymous environment, they will be denied access.


Request headers
~~~~~~~~~~~~~~~

When the environment variable is *not set at all*, we check the request headers.
We have two headers, to sidestep problems when a hacker manages to insert a header::

    X_DO_CHECK_ROLES
    X_DONT_CHECK_ROLES

The default is to deny the roles.  So:

- When none of these headers are set, we deny access to editors.

- When ``X_DO_CHECK_ROLES`` is set, we deny access to editors.

- When ``X_DONT_CHECK_ROLES`` is set, we allow access to all roles.

- When both headers are set, ``X_DO_CHECK_ROLES`` wins, and we deny access to editors.


Support
-------

If you are having issues, please let us know.
Contact Maurits van Rees at Zest Software, m.van.rees@zestsoftware.nl.
Or open an issue in `GitHub <https://github.com/collective/collective.denyroles/issues/>`_.


License
-------

The project is licensed under the GPLv2.
