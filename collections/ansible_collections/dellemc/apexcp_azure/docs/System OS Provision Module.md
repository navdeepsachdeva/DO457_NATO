System OS Provision Module for APEX Cloud Platform Azure
=================
### Product Guide

> © 2023 Dell Inc. or its subsidiaries. All rights reserved. Dell 
> EMC, and other trademarks are trademarks of Dell Inc. or its 
> subsidiaries. Other trademarks may be trademarks of their respective owners. 

Synopsis
--------
This module will install Azure Stack HCI OS on specified hosts.
  
Supported Endpoints
--------

* POST /system/initialize?mode=OS_PROVISION
* GET /system/initialize/status?mode=OS_PROVISION

Parameters
----------

<table  border=0 cellpadding=0 class="documentation-table">
    <tr>
        <th colspan="1">Parameter</th>
        <th>Choices/<font color="blue">Defaults</font></th>
                    <th width="100%">Comments</th>
    </tr>
    <tr>
        <td colspan="1">
            <div class="ansibleOptionAnchor" id="parameter-host_name"></div>
            <b>primary_host_ip</b>
            <a class="ansibleOptionLink" href="#parameter-host_name" title="Permalink to this option"></a>
            <div style="font-size: small">
                <span style="color: purple">type=string</span>
                <br>
                <span style="color: red">required=true</span>
            </div>
        </td>
        <td></td>
        <td>
            <div></div>
            <div>The primary node IP</div>
        </td>
    </tr>
    <tr>
        <td colspan="1">
            <div class="ansibleOptionAnchor" id="parameter-day1-json-file"></div>
            <b>day1_json_file</b>
            <a class="ansibleOptionLink" href="#parameter-day1-json-file" title="Permalink to this option"></a>
            <div style="font-size: small">
                <span style="color: purple">type=string</span>
                <br>
                <span style="color: red">required=true</span>
            </div>
        </td>
        <td></td>
        <td>
            <div></div>
            <div>The path of Day1 Json file</div>
        </td>
    </tr>
    <tr>
        <td colspan="1">
            <div class="ansibleOptionAnchor" id="parameter-state"></div>
            <b>timeout</b>
            <a class="ansibleOptionLink" href="#parameter-state" title="Permalink to this option"></a>
            <div style="font-size: small">
                <span style="color: purple">type=integer</span>
                <br>
                <span style="color: red"></span>
            </div>
        </td>
        <td><ul style="margin: 0; padding: 0"><b>Default:</b><li>7200s</li></ul></td>
        <td>
            <div></div>
            <div>Time out value for performing os provision, the default value is 7200 seconds</div>
            <div></div>
        </td>
    </tr>
</table>

Notes
-----
- Make sure your APEX Cloud Platform Azure environment supports the API that you use
- Details on execution of module dell_apexcp_azure_system_os_provision.py can be checked in the logs /tmp/apexcp_azure_system_os_provision.log

Examples
--------

``` yaml+jinja
  - name: Install Azure Stack HCI OS on specified nodes
    dell_apexcp_azure_system_os_provision:
        primary_host_ip: "{{ primary_host_ip }}"
        day1_json_file: "{{ day1_json_file }}"
        timeout: "{{ timeout }}"
```

Return Values
-------------

The following are the fields unique to this module:

<table border=0 cellpadding=0 class="documentation-table">
    <tr>
        <th colspan="2">Key</th>
        <th>Returned</th>
        <th width="100%">Description</th>
    </tr>
    <tr>
        <td colspan="2">
            <div class="ansibleOptionAnchor" id="return-changed"></div>
            <b>changed</b>
            <a class="ansibleOptionLink" href="#return-changed" title="Permalink to this return value"></a>
            <div style="font-size: small">
              <span style="color: purple">type=boolean</span>
            </div>
        </td>
        <td>always</td>
        <td><div>Whether or not the resource has changed.</div><br/></td>
    </tr>
    <tr>
        <td colspan="2">
            <div class="ansibleOptionAnchor" id="return-install-status"></div>
            <b>os_provision_result</b>
            <a class="ansibleOptionLink" href="#return-install-status" title="Permalink to this return value"></a>
            <div style="font-size: small"><span style="color: purple">type=dict</span></div>
        </td>
        <td>When calling the /system/initialize?mode=OS_PROVISION API is successful</td>
        <td><div></div><br/></td>
    </tr>
    <tr>
        <td class="elbow-placeholder"></td>
        <td colspan="1">
            <div class="ansibleOptionAnchor" id="return-install-status/request-id"></div>
            <b>request_id</b>
            <a class="ansibleOptionLink" href="#return-install-status/request-id" title="Permalink to this return value"></a>
            <div style="font-size: small"><span style="color: purple">type=string</span></div>
        </td>
        <td></td>
        <td><div>The task ID of OS provision.</div></td>
    </tr>
    <tr>
        <td class="elbow-placeholder">&nbsp;</td>
        <td colspan="1">
            <div class="ansibleOptionAnchor" id="return-install-status/status"></div>
            <b>status</b>
            <a class="ansibleOptionLink" href="#return-install-status/status" title="Permalink to this return value"></a>
            <div style="font-size: small"><span style="color: purple">type=string</span></div>
        </td>
        <td></td>
        <td><div>The OS provision result.</div></td>
    </tr>        
    <tr>
        <td class="elbow-placeholder">&nbsp;</td>
        <td colspan="1">
            <div class="ansibleOptionAnchor" id="return-install-status/detail"></div>
            <b>install_detail</b>
            <a class="ansibleOptionLink" href="#return-install-status/detail" title="Permalink to this return value"></a>
            <div style="font-size: small"><span style="color: purple">type=dict</span></div>
        </td>
        <td></td>
        <td><div>The OS provision detail.</div></td>
    </tr> 
    <tr>
        <td colspan="2">
            <div class="ansibleOptionAnchor" id="return-msg"></div>
            <b>msg</b>
            <a class="ansibleOptionLink" href="#return-msg" title="Permalink to this return value"></a>
            <div style="font-size: small"><span style="color: purple">type=string</span></div>
        </td>
        <td>Always</td>
        <td><div>The message for OS provision.</div></td>
    </tr>
</table>

Authors
-------

-   Dell APEX Cloud Platform for Microsoft Azure Ansible Development Team &lt;<ansible.team@dell.com>&gt;