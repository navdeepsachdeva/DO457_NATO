# Copyright (c) 2023 Dell Inc. or its subsidiaries. All Rights Reserved.
#
# This software contains the intellectual property of Dell Inc. or is licensed to Dell Inc. from third parties.
# Use of this software and the intellectual property contained therein is expressly limited to the terms and
# conditions of the License Agreement under which it is provided by or on
# behalf of Dell Inc. or its subsidiaries.
from __future__ import (absolute_import, division, print_function)

import logging
import ssl

import ansible_acp_azure_utility

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context
__metaclass__ = type

'''
This method is to initialize logger and return the logger object
parameters:
     - module_name: Name of module to be part of log message.
     - log_file_name: name of the file in which the log messages get
      appended.
     - log_devel: log level.
returns logger object
'''


def get_logger(module_name, log_file_name='/tmp/apexcp_azure_ansible.log', log_devel=logging.INFO):
    LOG_FILE_NAME = log_file_name
    LOG_FORMAT = CustomLogFormatter()
    LOGGER = logging.getLogger()
    LOGGER.setLevel(log_devel)

    # file output
    FILE_HANDLER = logging.FileHandler(LOG_FILE_NAME)
    FILE_HANDLER.setLevel(log_devel)
    FILE_HANDLER.setFormatter(LOG_FORMAT)
    LOGGER.addHandler(FILE_HANDLER)
    return LOGGER


class CustomLogFormatter(logging.Formatter):
    ''' Logging class for method '''
    info_fmt = "%(asctime)s [%(levelname)s]\t%(message)s"
    debug_fmt = "%(asctime)s [%(levelname)s]\t%(pathname)s:%(lineno)d\t%(message)s"

    def __init__(self, fmt="%(asctime)s [%(levelname)s]\t%(pathname)s:%(lineno)d\t%(message)s"):
        logging.Formatter.__init__(self, fmt)

    def format(self, record):
        if record.levelno == logging.INFO:
            self._fmt = CustomLogFormatter.info_fmt
            # python 3 compatibility
            if hasattr(self, '_style'):
                self._style._fmt = CustomLogFormatter.info_fmt
        else:
            self._fmt = CustomLogFormatter.debug_fmt
            # python 3 compatibility
            if hasattr(self, '_style'):
                self._style._fmt = CustomLogFormatter.debug_fmt
        result = logging.Formatter.format(self, record)
        return result


class BaseModule:
    def __init__(self, module):
        self.cloud_platform_manager_ip = module.params.get('cloud_platform_manager_ip')
        self.timeout = module.params.get('timeout')

    # Obtains the response for the given module path with specified api_version_number or highest found version
    def get_versioned_response(self, api_instance, module_path):
        return "v1"

    @staticmethod
    def create_configuration(host):
        configuration = ansible_acp_azure_utility.Configuration()
        configuration.verify_ssl = False
        configuration.host = f"https://{host}/rest/apex-cp"
        return configuration
