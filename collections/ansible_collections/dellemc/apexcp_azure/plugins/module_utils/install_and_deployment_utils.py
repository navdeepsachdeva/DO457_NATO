# Copyright (c) 2023 Dell Inc. or its subsidiaries. All Rights Reserved.
#
# This software contains the intellectual property of Dell Inc. or is licensed to Dell Inc. from third parties.
# Use of this software and the intellectual property contained therein is expressly limited to the terms and
# conditions of the License Agreement under which it is provided by or on
# behalf of Dell Inc. or its subsidiaries.

import json
import os
import time

import ansible_acp_azure_utility
import urllib3
from ansible_acp_azure_utility.rest import ApiException

from . import dell_apexcp_azure_ansible_utils as utils
from .dell_apexcp_azure_ansible_utils import BaseModule

CHECK_STATUS_INTERVAL = 60
MAX_ERROR_COUNT = 10
TIMEOUT_OS_PROVISION = 7200
MAX_ERROR_COUNT_OS_PROVISION = 90


def create_installation_and_deployment_api(ip):
    return ansible_acp_azure_utility.InstallationAndDeploymentOfTheAPEXCloudPlatformForMicrosoftAzureApi(
        ansible_acp_azure_utility.ApiClient(BaseModule.create_configuration(ip)))


MODE_OS_PROVISION = "OS_PROVISION"
MODE_LTP_REGISTRATION = "LTP_REGISTRATION"
MODE_CLOUD_DEPLOYMENT = "CLUSTER_DEPLOYMENT"


class SystemInitializeTask(utils.BaseModule):

    def __init__(self, module, logger, mode):
        super().__init__(module=module)
        self.day1_json_file = module.params.get('day1_json_file')
        self.primary_host_ip = module.params.get('primary_host_ip')
        self.logger = logger
        self.logger.info(f"{self.timeout},{self.day1_json_file}")
        self.mode = mode
        self.json_payload = None

    def validate_input(self,module):
        file = self.day1_json_file
        if os.path.isfile(file):
            with open(file, encoding='utf_8') as f:
                config_json = json.load(f)
                cloud_platform_manager_ip = config_json.get("cloud_platform_manager", {}).get("ip")
                self.json_payload = config_json
                if not cloud_platform_manager_ip:
                    self.logger.error('ACP manager IP not found in day1 json file, please verify and try again')
                    module.fail_json(msg="ACP manager IP not found in day1 json file!")
                    return False
                else:
                    self.cloud_platform_manager_ip = cloud_platform_manager_ip
        else:
            self.logger.error('Day1 json file cannot not be opened or does not exit, please verify and try again')
            module.fail_json(msg="Day1 json file not found!")
            return False
        return True

    def start(self):
        if self.mode == MODE_OS_PROVISION:
            api_instance = create_installation_and_deployment_api(self.primary_host_ip)
        else:
            api_instance = create_installation_and_deployment_api(self.cloud_platform_manager_ip)
        try:
            # start day1 FirstRun(ex:v1_system_initialize_post)
            call_string = 'v2_system_initialize_post'
            self.logger.info(f"Trigger system initialize start(mode={self.mode})")
            api_initialize_post = getattr(api_instance, call_string)
            response = api_initialize_post(self.json_payload, mode=self.mode)
            job_id = response.request_id
            self.logger.info(f"Trigger system initialize done(job id={job_id})")
            return job_id
        except ApiException as e:
            self.logger.error("Exception when calling v2_system_initialize_post: %s\n", e)
            return 'error'

    def get_request_status_from_primary_node(self):
        # create an instance of the API class
        api_instance_for_primary_host = create_installation_and_deployment_api(self.primary_host_ip)
        call_string = 'v2_system_initialize_status_get'
        try:
            api_system_initialize_status_get = getattr(api_instance_for_primary_host, call_string)
            response = api_system_initialize_status_get(mode="OS_PROVISION", _request_timeout=(3, 60))
            return response
        except Exception as e:
            self.logger.error("Exception when calling v2_system_initialize_status_get: %s\n", e.__str__())
        return None

    def get_request_status(self):
        # create an instance of the API class
        api_instance = create_installation_and_deployment_api(self.cloud_platform_manager_ip)

        # get system initialize status(ex:v2_system_initialize_status_get)
        call_string = 'v2_system_initialize_status_get'
        try:
            api_system_initialize_status_get = getattr(api_instance, call_string)
            return api_system_initialize_status_get(mode=self.mode)
        except Exception as e:
            self.logger.error("Exception when calling v2_system_initialize_status_get: %s\n", e)
            return None

    def check_task_status(self, task_status):
        is_validation_task = False
        # check the last task is a validation task or not
        if task_status.extension and task_status.extension.steps and task_status.extension.steps[-1].name:
            last_step = task_status.extension.steps[-1].name.lower()
            self.logger.info("last step: %s", last_step)
            # check whether last step contains "validator"
            if "validator" in last_step or "validation" in last_step:
                is_validation_task = True

        if not is_validation_task:
            return task_status.state
        else:
            # If the validation is ongoing, we will wait for it to complete
            if task_status.state == "STARTED":
                return "VALIDATING"
            else:
                # if the validation is completed or failed, we will continue to the next task
                return "NOT_STARTED"

    def check_current_status(self):
        task_status = self.get_request_status()
        if task_status and task_status.state:
            return self.check_task_status(task_status)

        if self.mode == MODE_OS_PROVISION:
            task_status = self.get_request_status_from_primary_node()
            if task_status and task_status.state:
                return self.check_task_status(task_status)

        return "NOT_STARTED"

    def check_task_progress(self):
        time_out = 0
        error_count = 0
        status = ""
        initialize_response = None
        initial_timeout = self.timeout
        last_install_response = None
        while status not in (
                'COMPLETED', 'FAILED') and time_out < self.timeout and error_count < MAX_ERROR_COUNT:
            initialize_response = self.get_request_status()
            if initialize_response:
                error_count = 0
                status = initialize_response.state
                last_install_response = initialize_response
                self.logger.info(f"The {self.mode} is ongoing,progress:{initialize_response.progress}%")
            else:
                error_count += 1
                self.logger.info(f'Fail to get {self.mode} status. Count: %s', error_count)

            time.sleep(CHECK_STATUS_INTERVAL)
            time_out = time_out + CHECK_STATUS_INTERVAL
        if last_install_response:
            self.logger.info(f'The {self.mode} result -> %s.', initialize_response)
        if error_count >= MAX_ERROR_COUNT:
            self.logger.info(f"Exceeded the max error count while checking {self.mode} progress")
        if time_out >= initial_timeout:
            self.logger.info(f"{self.mode} is timeout")
        return status

    def check_os_provision_status(self):
        error_count = 0
        os_provision_status = ""
        time_out = 0
        installation_response = None
        last_os_provision_response = None
        # primary node is installing or installed, means the day1 service will not be able to connect
        primary_node_installing = False
        while (os_provision_status not in ('COMPLETED', 'FAILED') and
               time_out < TIMEOUT_OS_PROVISION and error_count < MAX_ERROR_COUNT_OS_PROVISION):
            if primary_node_installing:
                installation_response = self.get_request_status()
            else:
                installation_response = self.get_request_status_from_primary_node()
                if not installation_response:
                    primary_node_installing = True

            if installation_response:
                error_count = 0
                os_provision_status = installation_response.state
                last_os_provision_response = installation_response
                self.logger.info('OS provision task status: %s.', os_provision_status)
            else:
                if primary_node_installing:
                    self.logger.info(f"Waiting for APEX cloud manager host up(error count:{error_count})")
                error_count += 1

            time.sleep(CHECK_STATUS_INTERVAL)
            time_out = time_out + CHECK_STATUS_INTERVAL
        install_detail = None
        if installation_response and installation_response.detail:
            detail = installation_response.detail
            install_detail = json.loads(detail)
        if last_os_provision_response:
            self.logger.info(f"The last os provision response:{last_os_provision_response}")
        return os_provision_status, install_detail


