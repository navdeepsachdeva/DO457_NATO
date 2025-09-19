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
module: dell_apexcp_azure_initialize_ldaps_cert

short_description: Initialize LDAPS certificate.

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description:
- This module will initialize LDAPS certificate before starting LTP registration.
options:
  cloud_platform_manager_ip:
    description:
      The ip address of APEX Cloud Platform Manager.
    required: True
    type: str

  ldaps_cert_file:
    description:
      The path of LDAPS certificate file
    required: True
    type: str

author:
    - Apex Cloud Platform Ansible Development Team(@xxxx) <ansible.team@dell.com>

'''

EXAMPLES = r'''
- name: Initialize LDAPs certificate
  dell_apexcp_azure_initialize_ldaps_cert:
    cloud_platform_manager_ip: "{{ cloud_platform_manager_ip }}"
    ldaps_cert_file: "{{ ldaps_cert_file }}"
'''

RETURN = r'''
changed:
    description: Whether or not the resource has changed.
    returned: always
    type: bool
initialize_cert_result:
  description: The result of LDAPS certificate initialization.
  returned: always
  type: string
msg:
  description: The message of LDAPS certificate initialization.
  returned: always
  type: string
  sample: >-
    {
      "changed": true,
      "initialize_cert_result": "SUCCESS",
      "msg": "Initialize LDAPS certificate is successful. Please see the /tmp/apexcp_azure_initialize_ldaps_cert.log for more details"
    }
'''


import urllib3
from ansible.module_utils.basic import AnsibleModule
import json
import os
from ansible_collections.dellemc.apexcp_azure.plugins.module_utils import dell_apexcp_azure_ansible_utils as utils
from ansible_collections.dellemc.apexcp_azure.plugins.module_utils import auth_api_utils
# from plugins.module_utils import dell_apexcp_azure_initialize_ldaps_cert_utils as utils

log_file_name = "/tmp/apexcp_azure_initialize_ldaps_cert.log"
LOGGER = utils.get_logger(module_name="dell_apexcp_azure_initialize_ldaps_cert",
                          log_file_name=log_file_name)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def main():
    ''' Entry point into execution flow '''
    global module
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        cloud_platform_manager_ip=dict(required=True),
        root_ldaps_cert_file=dict(required=True),
        intermediate_cert_files=dict(required=False),
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )
    LOGGER.info(f'The parameter is {json.dumps(module.params)}')
    intermediate_cert_files = module.params.get('intermediate_cert_files')
    intermediate_cert_file_contents = []
    if intermediate_cert_files:
        intermediate_cert_files = intermediate_cert_files.split(",")
        for f in intermediate_cert_files:
            if os.path.isfile(f):
                with open(f, encoding='utf_8') as fs:
                    intermediate_cert_file_contents.append("".join(fs.readlines()))
            else:
                LOGGER.info(f'Intermediate certificate file {f} not exist.')
                module.fail_json(msg=f"Intermediate certificate file {f} not found!")

    file = module.params.get('root_ldaps_cert_file')
    if os.path.isfile(file):
        LOGGER.info('Initialize LDAPS certificate by using file %s', file)
        with open(file, encoding='utf_8') as f:
            ldaps_cert_content = "".join(f.readlines())
    else:
        LOGGER.error('Root certificate file cannot not be opened or does not exit, please verify and try again')
        module.fail_json(msg="Root certificate file not found!")

    LOGGER.info("----Initialize LDAPS certificate----")
    response = auth_api_utils.InitializeLdapsCert(module, LOGGER).initialize_cert(ldaps_cert_content,
                                                                                  intermediate_cert_file_contents)
    LOGGER.info(f"----Result of initialize LDAPS certificate {response}-----")
    if response == "error":
        module.fail_json(
            msg=f"Call initialize LDAPS certificate API failed. Please see the {log_file_name} for more details")

    if response.result == 'SUCCESS':
        facts_result = dict(changed=True, initialize_cert_result=response.result,
                            msg=f"Initialize LDAPS certificate is successful. Please see the {log_file_name} for more details")
        module.exit_json(**facts_result)
    else:
        facts_result = dict(failed=True, initialize_cert_result=response.result,
                               msg=f'Initialize LDAPS certificate failed. Please see the {log_file_name} for more details')
        module.exit_json(**facts_result)


if __name__ == '__main__':
    main()
