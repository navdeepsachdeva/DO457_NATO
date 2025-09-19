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
module: dell_apexcp_azure_cluster_deployment

short_description: Perform the cluster deployment of a Anacortes Cluster

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description:
- This module will configure and deploy a new APEX Cloud Platform cluster 
  for Microsoft Azure based on the provided day1 json file.
options:
  day1_json_file:
    description:
      The path of Day1 Json file.
    required: True
    type: str

  timeout:
    description:
      Time out value for cluster deployment, the default value is 36000 seconds
    required: false
    type: int
    default: 36000

author:
    - Apex Cloud Platform Ansible Development Team(@xxxx) <ansible.team@dell.com>

'''

EXAMPLES = r'''
- name: Configure and deploy a new APEX Cloud Platform cluster for Azure
  dell_apexcp_azure_cluster_deployment:
    day1_json_file: "{{ day1_json_file }}"
'''

RETURN = r'''
changed:
    description: Whether or not the resource has changed.
    returned: always
    type: bool
cluster_deployment_result:
  description: Cluster deployment status summary
  returned: always
  type: dict
  sample: >-
   {
    "cluster_deployment_result": {
        "request_id": "433d0a61-06e7-4cb8-a1eb-985ab9a8b5dd",
        "status": "COMPLETED"
    }
    "msg": "Cluster deployment is successful. Please see the /tmp/apexcp_azure_cluster_deployment.log for more details"
   }
'''

import urllib3
from ansible.module_utils.basic import AnsibleModule

import json

# from plugins.module_utils import dell_apexcp_azure_ansible_utils as utils
# from plugins.module_utils import install_and_deployment_utils
from ansible_collections.dellemc.apexcp_azure.plugins.module_utils import dell_apexcp_azure_ansible_utils as utils
from ansible_collections.dellemc.apexcp_azure.plugins.module_utils import install_and_deployment_utils

# from plugins.module_utils import dell_apexcp_azure_ansible_utils as utils

log_file_name = "/tmp/apexcp_azure_cluster_deployment.log"
LOGGER = utils.get_logger(module_name="dell_apexcp_azure_cluster_deployment",
                          log_file_name=log_file_name)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

MAX_ERROR_COUNT = 10
CHECK_STATUS_INTERVAL = 60
MAX_CHECK_COUNT = 600


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
    LOGGER.info(f'The parameter is {json.dumps(module.params)}')
    cloud_deployment_task = install_and_deployment_utils.SystemInitializeTask(module, LOGGER,
                                                                              mode=install_and_deployment_utils.MODE_CLOUD_DEPLOYMENT)
    cloud_deployment_task.validate_input(module)
    current_status = cloud_deployment_task.check_current_status()
    installation_request_id = None
    if current_status == "COMPLETED":
        LOGGER.info("-----The cluster has been deployed,exit-----")
        cluster_deployment_result = {'status': current_status}
        facts_result = dict(changed=False, cluster_deployment_result=cluster_deployment_result,
                            msg=f"Cluster deployment completed. Please see the {log_file_name} for more details")
        module.exit_json(**facts_result)
    elif current_status == "VALIDATING":
        LOGGER.info("A validation task is ongoing,wait for the task to complete")
        module.fail_json(msg="A validation task is ongoing,wait for the task to complete.")
    elif current_status in ("NOT_STARTED", "FAILED"):
        LOGGER.info("----Configure and deploy a new APEX Azure cluster----")
        installation_request_id = cloud_deployment_task.start()
        LOGGER.info('Cluster deployment task ID: %s.', installation_request_id)
        if installation_request_id == "error":
            LOGGER.info("------Cluster deployment task startup failed-----")
            module.fail_json(
                msg=f"Cluster deployment task startup failed. Please see the {log_file_name} for more details")
    installation_status = cloud_deployment_task.check_task_progress()
    if installation_status == 'COMPLETED':
        LOGGER.info("Cluster deployment completed")
        cluster_deployment_result = {'status': installation_status, 'request_id': installation_request_id}
        facts_result = dict(changed=True, cluster_deployment_result=cluster_deployment_result,
                            msg=f"Cluster deployment is successful. Please see the {log_file_name} for more details")
        module.exit_json(**facts_result)
    else:
        LOGGER.info("------Cluster deployment failed-----")
        cluster_deployment_result = {'request_id': installation_request_id}
        facts_result = dict(failed=True, cluster_deployment_result=cluster_deployment_result,
                               msg=f'Cluster deployment has failed. Please see the {log_file_name} for more details')
        module.exit_json(**facts_result)


if __name__ == '__main__':
    main()
