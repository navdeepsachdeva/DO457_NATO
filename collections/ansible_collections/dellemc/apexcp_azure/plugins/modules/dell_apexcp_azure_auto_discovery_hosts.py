# Copyright (c) 2023 Dell Inc. or its subsidiaries. All Rights Reserved.
#
# This software contains the intellectual property of Dell Inc. or is licensed to Dell Inc. from third parties.
# Use of this software and the intellectual property contained therein is expressly limited to the terms and
# conditions of the License Agreement under which it is provided by or on
# behalf of Dell Inc. or its subsidiaries.
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: dell_apexcp_azure_auto_discovery_hosts

short_description: Get auto-discovered nodes.

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description:
- This module will Get Auto-discovered Nodes before os provisioning. 
options:
  primary_host_ip:
    description:
      The primary node IP
    required: True
    type: str

  timeout:
    description:
      Time out value for Day1 bring up, the default value is 60 seconds
    required: false
    type: int
    default: 60

author:
    - Apex Cloud Platform Ansible Development Team(@xxxx) <ansible.team@dell.com>

'''

EXAMPLES = r'''
- name: Get Auto-discovered Nodes During Bootstrap
  dell_apexcp_azure_auto_discovery_hosts:
    primary_host_ip: "{{ primary_host_ip }}"
'''

RETURN = r'''
System_Initialize_Nodes_Information:
  description: Get Auto-discovered Nodes before os provisioning.
  returned: always
  type: dict
  sample: >-
    {
    "System_Initialize_Nodes_Information": {
        "bootstrap_os_version": "1.1.21",
        "hostname": "localhost",
        "ipv6": "fe80::b645:6ff:feec:5577%eth1.3939",
        "model": "APEX MC-4510c",
        "primary": true,
        "serial_number": "FKBNDX3"
      }
    }
'''

import urllib3
from ansible.module_utils.basic import AnsibleModule
import ansible_acp_azure_utility

# from plugins.module_utils import dell_apexcp_azure_ansible_utils as utils
from ansible_collections.dellemc.apexcp_azure.plugins.module_utils import dell_apexcp_azure_ansible_utils as utils

logger_file = "/tmp/apexcp_azure_auto_discovery_host.log"

LOGGER = utils.get_logger(module_name="dell_apexcp_azure_auto_discovery_hosts",
                          log_file_name=logger_file)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class SystemInitialize(utils.BaseModule):
    def __init__(self):
        super().__init__(module=module)
        self.primary_host_ip = module.params.get('primary_host_ip')
        LOGGER.info(f"{self.primary_host_ip}, {self.timeout}")

    def get_system_initialize_nodes(self):
        # create an instance of the API class
        api_instance_for_primary_host = ansible_acp_azure_utility.InstallationAndDeploymentOfTheAPEXCloudPlatformForMicrosoftAzureApi(
            ansible_acp_azure_utility.ApiClient(SystemInitialize.create_configuration(self.primary_host_ip)))
        self.api_version_string = self.get_versioned_response(api_instance_for_primary_host, 'Get /system/initialize/nodes')
        call_string = self.api_version_string + '_system_initialize_nodes_get'
        LOGGER.info("Using utility method: %s\n", call_string)
        api_system_initialize_nodes_get = getattr(api_instance_for_primary_host, call_string)
        try:
            # get initialize nodes
            response = api_system_initialize_nodes_get(_request_timeout=60)
        except Exception as e:
            LOGGER.error(
                "Exception when calling InstallationAndDeploymentOfAPEXCloudPlatformForMicrosoftAzureApi->%s_system_initialize_nodes_get: %s\n",
                self.api_version_string, e)
            return 'error'
        LOGGER.info("%s/system/initialize/nodes api response: %s\n", self.api_version_string, response)
        if response:
          return self._generate_initialize_nodes_info_from_response_data(response)

    def _generate_initialize_nodes_info_from_response_data(self, res):
        initialize_nodes_info_response = {}
        nm = 0
        try:
          for node in res:
            nm += 1
            node_nm = f"node_{nm}"
            node_info = {}
            node_info['model'] = node.model
            node_info['serial_number'] = node.serial_number
            node_info['hostname'] = node.hostname
            node_info['primary'] = node.primary
            node_info['ipv6'] = node.ipv6
            node_info['bootstrap_os_version'] = node.bootstrap_os_version
            initialize_nodes_info_response[node_nm] = node_info
        except Exception as e:
            LOGGER.error(
                "Load response data failed: %s\n", e)
            return 'error'
        return initialize_nodes_info_response

def main():
    ''' Entry point into execution flow '''
    global module
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        primary_host_ip=dict(required=True),
        timeout=dict(type='int', default=60)
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    result = SystemInitialize().get_system_initialize_nodes()
    if result == 'error':
        module.fail_json(
            msg=f"API system/initialize/nodes call failed, Please see the {logger_file} for more details")
    LOGGER.info("result: %s\n", result)
    if result:
        LOGGER.info("-----Initialize Nodes GET Successfully-----")
        msg = f'Get auto-discovered nodes is successful. Please see the {logger_file} for more details'
    else:
        LOGGER.info("-----Initialize Nodes GET Failed-----")
        msg = f'Get auto-discovered nodes failed. Please see the {logger_file} for more details'
    az_facts = {'System_Initialize_Nodes_Information': result}
    az_facts_result = dict(changed=False, System_Initialize_Nodes_API=az_facts, msg=msg)
    module.exit_json(**az_facts_result)


if __name__ == '__main__':
    main()