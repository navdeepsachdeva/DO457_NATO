# Copyright (c) 2023 Dell Inc. or its subsidiaries. All Rights Reserved.
#
# This software contains the intellectual property of Dell Inc. or is licensed to Dell Inc. from third parties.
# Use of this software and the intellectual property contained therein is expressly limited to the terms and
# conditions of the License Agreement under which it is provided by or on
# behalf of Dell Inc. or its subsidiaries.

import ansible_acp_azure_utility
from ansible_acp_azure_utility.rest import ApiException

from . import dell_apexcp_azure_ansible_utils as utils


class InitializeLdapsCert(utils.BaseModule):

    def __init__(self, module, logger):
        super().__init__(module=module)
        self.ldaps_cert_file = module.params.get('ldaps_cert_file')
        self.logger = logger
        logger.info(f"{self.cloud_platform_manager_ip},{self.ldaps_cert_file}")

    def initialize_cert(self, ldaps_cert_content, intermediate_cert_file_contents):
        payload = [
            {
                "cert_type": "ROOT",
                "cert": f"{ldaps_cert_content.strip()}"
            }
        ]
        for c in intermediate_cert_file_contents:
            payload.append({
                "cert_type": "INTERMEDIATE",
                "cert": f"{c.strip()}"
            })
        # create an instance of the API class
        api_instance = ansible_acp_azure_utility.AuthenticationOfAPEXCloudPlatformManagerApi(
            ansible_acp_azure_utility.ApiClient(InitializeLdapsCert.create_configuration(self.cloud_platform_manager_ip)))
        try:
            # start initialize cert
            call_string = self.get_versioned_response(api_instance, 'Post /ldaps-certs/initialize') + '_cert_initialize_post'
            self.logger.info("Using utility method: %s\n", call_string)
            api_cert_initialize_post = getattr(api_instance, call_string)
            return api_cert_initialize_post(payload)
        except ApiException as e:
            self.logger.error("Exception when calling v1_cert_initialize_post: %s\n", e)
            return "error"

