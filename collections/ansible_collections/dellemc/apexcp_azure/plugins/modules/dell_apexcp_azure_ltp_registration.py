# Copyright (c) 2024 Dell Inc. or its subsidiaries. All Rights Reserved.
#
# This software contains the intellectual property of Dell Inc. or is licensed to Dell Inc. from third parties.
# Use of this software and the intellectual property contained therein is expressly limited to the terms and
# conditions of the License Agreement under which it is provided by or on
# behalf of Dell Inc. or its subsidiaries.
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: dell_apexcp_azure_ltp_registration

short_description: Register specified nodes to Azure portal.

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.1.0"

description:
- This module will register specified nodes to Azure portal.
options:
  day1_json_file:
    description:
      The path of Day1 Json file.
    required: True
    type: str

  timeout:
    description:
      Time out value for LTP registration, the default value is 7200 seconds
    required: false
    type: int
    default: 7200
    
author:
    - Apex Cloud Platform Ansible Development Team(@xxxx) <ansible.team@dell.com>

'''

EXAMPLES = r'''
- name: Perform LTP registration for specified nodes
  dell_apexcp_azure_ltp_registration:
    day1_json_file: "{{ day1_json_file }}"
'''

RETURN = r'''
changed:
    description: Whether or not the resource has changed.
    returned: always
    type: bool
ltp_registration_result:
  description: The result of LTP registration.
  returned: always
  type: dict
msg:
  description: The message of LTP registration.
  returned: always
  type: string
  sample: >-
    {
      "changed": true,
      "ltp_registration_result": {
        "request_id": "433d0a61-06e7-4cb8-a1eb-985ab9a8b5dd",
        "status": "COMPLETED"
      }
      "msg": "LTP registration is successful. Please see the /tmp/apexcp_azure_ltp_registration.log for more details"
    }
'''


import urllib3
from ansible.module_utils.basic import AnsibleModule

# from plugins.module_utils import dell_apexcp_azure_ansible_utils as utils
# from plugins.module_utils import install_and_deployment_utils
from ansible_collections.dellemc.apexcp_azure.plugins.module_utils import dell_apexcp_azure_ansible_utils as utils
from ansible_collections.dellemc.apexcp_azure.plugins.module_utils import install_and_deployment_utils


log_file_name = "/tmp/apexcp_azure_ltp_registration.log"
LOGGER = utils.get_logger(module_name="dell_apexcp_azure_ltp_registration",
                          log_file_name=log_file_name)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


MAX_ERROR_COUNT = 10
CHECK_STATUS_INTERVAL = 60
MAX_CHECK_COUNT = 120


def main():
    ''' Entry point into execution flow '''
    global module
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        cloud_platform_manager_ip=dict(required=False),
        day1_json_file=dict(required=True),
        timeout=dict(type='int', default=MAX_CHECK_COUNT * CHECK_STATUS_INTERVAL)
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    ltp_registration = install_and_deployment_utils.SystemInitializeTask(module, LOGGER,
                                                                         mode=install_and_deployment_utils.MODE_LTP_REGISTRATION)
    ltp_registration.validate_input(module)
    current_status = ltp_registration.check_current_status()
    request_id = None
    if current_status == "COMPLETED":
        LOGGER.info("-----The LTP registration is done,exit-----")
        ltp_registration_result = {'status': current_status}
        facts_result = dict(changed=False, ltp_registration_result=ltp_registration_result,
                            msg=f"The LTP registration completed. Please see the {log_file_name} for more details")
        module.exit_json(**facts_result)
    elif current_status == "VALIDATING":
        LOGGER.warn("A validation task is ongoing,wait for the task to complete")
        module.fail_json(msg="A validation task is ongoing,exit.")
    elif current_status in ("NOT_STARTED", "FAILED"):
        LOGGER.info("LTP registration start")
        request_id = ltp_registration.start()
        LOGGER.info('Task ID: %s.', request_id)
        if request_id == "error":
            LOGGER.info("LTP registration task startup failed.")
            module.fail_json(
                msg=f"LTP registration task startup failed. Please see the {log_file_name} for more details")
    ltp_registration_status = ltp_registration.check_task_progress()
    if ltp_registration_status == 'COMPLETED':
        LOGGER.info("LTP registration completed")
        ltp_registration_result = {'status': ltp_registration_status, 'request_id': request_id}
        facts_result = dict(changed=True, ltp_registration_result=ltp_registration_result,
                            msg=f"LTP registration is successful. Please see the {log_file_name} for more details")
        module.exit_json(**facts_result)
    else:
        LOGGER.info("LTP registration failed")
        ltp_registration_result = {'request_id': request_id}
        facts_result = dict(failed=True, ltp_registration_result=ltp_registration_result,
                            msg=f'LTP registration has failed. Please see the {log_file_name} for more details')
        module.exit_json(**facts_result)


if __name__ == '__main__':
    main()