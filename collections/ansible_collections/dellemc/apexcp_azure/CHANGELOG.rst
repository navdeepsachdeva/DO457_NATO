=============================================
Dell APEX Cloud Platform for Microsoft Azure
=============================================

.. contents:: Topics

v1.1.0
======

Release Summary
---------------

- The ``dell_apexcp_azure_ltp_registration`` module is added to register specified nodes to Azure portal.
- The ``dell_apexcp_azure_cluster_deployment`` module is updated to remove the upload of LDAPs certificate file.
- The ``dell_apexcp_azure_system_initialize_full`` module is removed.

Major Changes
-------------

- LTP Registration - This module allows to register specified nodes to Azure portal.
- Upgrade API "system/initialize" API to v2
- Remove the module of ``dell_apexcp_azure_system_initialize_full``.

Minor Changes
-------------

- Initialize LDAPS Certificate - This module is enhanced to support the upload of intermediate certificate files.
