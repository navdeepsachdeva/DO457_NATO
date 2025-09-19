# Ansible Modules for Dell APEX Cloud Platform for Microsoft Azure
The Ansible Modules for Dell APEX Cloud Platform for Microsoft Azure allow data center and IT administrators to use RedHat Ansible to automate and orchestrate the configuration and management of Dell APEX Cloud Platform for Microsoft Azure.

The capabilities of Ansible modules are gathering system information and performing Day1 Initialization. These tasks can be executed by running simple playbooks written in yaml syntax. The modules are written so that all the operations are idempotent, therefore making multiple identical requests has the same effect as making a single request.

## Support
Ansible modules for Dell APEX Cloud Platform for Microsoft Azure are supported by Dell EMC open source community, but not product support agreements, and are provided under the terms of the license attached to the source code. Dell EMC does not provide support for any source code modifications. For any Ansible module issues, questions or feedback, join the [Dell EMC Automation community]( https://www.dell.com/community/Automation/bd-p/Automation ).

## Supported Platforms
* Dell APEX Cloud Platform for Microsoft Azure

## Prerequisites
This table provides information about the software prerequisites for the Ansible Modules for Dell EMC VxRail.

| **Ansible Modules** | **APEX Cloud Platform for Microsoft Azure version** | **Python version** | **Python library (ACP Ansible Azure Utility) version** | **Ansible Version** |
|---------------------|-----------------------------------------------------|---------------|--------------------------------------------------------|---------------------|
| v1.1.0 | 01.03.00.00 | 3.8 | 1.1.0 | 2.13 |

* Please follow Dell APEX Cloud Platform for Microsoft Azure Ansible Utility installation instructions on [Dell APEX Cloud Platform for Microsoft Azure Ansible Utility Documentation](https://github.com/dell/ansible-acp-azure-utility)

## Idempotency
The modules are written in such a way that all requests are idempotent and hence fault-tolerant. This means that the result of a successfully performed request is independent of the number of times it is executed.

## List of Ansible Modules for Dell APEX Cloud Platform for Microsoft Azure
* [Auto Discovery Hosts Module](./docs/Auto%20Discovery%20Hosts%20Module.md)
* [System OS Provision Module](./docs/System%20OS%20Provision%20Module.md)
* [Initialize LDAPS Certificate Module](./docs/Initialize%20LDAPs%20Certificate%20Module.md)
* [LTP Registration Module](./docs/LTP%20Registration%20Module.md)
* [Cluster Deployment Module](./docs/Cluster%20Deployment%20Module.md)

## Installation of SDK

Install the python sdk named ['Dell APEX Cloud Platform for Microsoft Azure Ansible Utility'](https://github.com/dell/ansible-acp-azure-utility). It can be installed using pip, based on the appropriate python version.

## Installing Collections

* Download the tar build and install the collection anywhere in your system, e.g.

      ansible-galaxy collection install dellemc-apexcp_azure-1.1.0.tar.gz -p <install_path>

* Set the environment variable:

      export ANSIBLE_COLLECTIONS_PATHS=$ANSIBLE_COLLECTIONS_PATHS:<install_path>

## Using Collections

* In order to use any Ansible module, ensure that the importation of the proper FQCN (Fully Qualified Collection Name) must be embedded in the playbook. For example,
  <br>collections:
  <br>&nbsp;&nbsp;&nbsp; - dellemc.apexcp_azure
* To generate Ansible documentation for a specific module, embed the FQCN before the module name. For example,
  <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *ansible-doc dellemc.apexcp_azure.dell_apexcp_azure_cluster_deployment*

## Running Ansible Modules

The Ansible server must be configured with Python library for Dell APEX Cloud Platform for Microsoft Azure Ansible Utility to run the Ansible playbooks. The [Documents]( https://github.com/dell/ansible-acp-azure/tree/master/docs ) provide information on different Ansible modules along with their functions and syntax. The parameters table in the Product Guide provides information on various parameters which needs to be configured before running the modules.
