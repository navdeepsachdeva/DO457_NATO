Initialize LDAPs Certificate Module for APEX Cloud Platform Azure
=================
### Product Guide

> © 2023 Dell Inc. or its subsidiaries. All rights reserved. Dell 
> EMC, and other trademarks are trademarks of Dell Inc. or its 
> subsidiaries. Other trademarks may be trademarks of their respective owners. 

Synopsis
--------
This module will import LDAPs certificate to APEX Cloud Platform Manager before starting cluster deployment.
  
Supported Endpoints
--------

* POST /ldaps-certs/initialize 

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
            <div class="ansibleOptionAnchor" id="parameter-cloud-platform-manager-ip"></div>
            <b>cloud_platform_manager_ip</b>
            <a class="ansibleOptionLink" href="#parameter-cloud-platform-manager-ip" title="Permalink to this option"></a>
            <div style="font-size: small">
                <span style="color: purple">type=string</span>
                <br>
                <span style="color: red">required=true</span>
            </div>
        </td>
        <td></td>
        <td><div>The ip address of APEX Cloud Platform Manager</div></td>
    </tr>
    <tr>
        <td colspan="1">
            <div class="ansibleOptionAnchor" id="parameter-ldaps-cert-file"></div>
            <b>root_ldaps_cert_file</b>
            <a class="ansibleOptionLink" href="#parameter-ldaps-cert-file" title="Permalink to this option"></a>
            <div style="font-size: small">
                <span style="color: purple">type=string</span>
                <br>
                <span style="color: red">required=true</span>
            </div>
        </td>
        <td></td>
        <td>
            <div></div>
            <div>The path of root LDAPs certificate file</div>
        </td>
    </tr>
    <tr>
        <td colspan="1">
            <div class="ansibleOptionAnchor" id="parameter-ldaps-cert-file"></div>
            <b>intermediate_cert_files</b>
            <a class="ansibleOptionLink" href="#parameter-ldaps-cert-file" title="Permalink to this option"></a>
            <div style="font-size: small">
                <span style="color: purple">type=string</span>
                <br>
                <span style="color: red">required=false</span>
            </div>
        </td>
        <td></td>
        <td>
            <div></div>
            <div>The path of intermediate LDAPs certificate files<br>
                If there are multiple intermediate LDAPs certificate files, separate them with comma.<br>
                If there is no intermediate LDAPs certificate file, leave it blank.
            </div>
        </td>
    </tr>

</table>

Notes
-----
- Make sure your APEX Cloud Platform Azure environment supports the API that you use
- Details on execution of module dell_apexcp_azure_initialize_ldaps_cert.py can be checked in the logs /tmp/apexcp_azure_initialize_ldaps_cert.log

Examples
--------

``` yaml+jinja
  - name: Initialize LDAPs certificate
    dell_apexcp_azure_initialize_ldaps_cert:
        cloud_platform_manager_ip: "{{ cloud_platform_manager_ip }}"
        root_ldaps_cert_file: "{{ ldaps_cert_file }}"
        intermediate_cert_files: "{{ intermediate_cert_files }}"
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
            <div style="font-size: small"><span style="color: purple">type=boolean</span></div>
        </td>
        <td>Always</td>
        <td>
            <div>Whether or not the resource has changed.</div><br/>
        </td>
    </tr>
    <tr>
        <td colspan="2">
            <div class="ansibleOptionAnchor" id="return-initialize-cert-result"></div>
            <b>initialize_cert_result</b>
            <a class="ansibleOptionLink" href="#return-initialize-cert-result" title="Permalink to this return value"></a>
            <div style="font-size: small"><span style="color: purple">type=string</span></div>
        </td>
        <td>When LDAPS certificate initialization is successful</td>
        <td><div>The result of LDAPs certificate initialization</div><br/></td>
    </tr>
    <tr>
        <td colspan="2">
            <div class="ansibleOptionAnchor" id="return-msg"></div>
            <b>msg</b>
            <a class="ansibleOptionLink" href="#return-msg" title="Permalink to this return value"></a>
            <div style="font-size: small">
              <span style="color: purple">type=string</span>
            </div>
        </td>
        <td>Always</td>
        <td><div>The message for LDAPs certificate initialization</div></td>
    </tr>
</table>

Authors
-------

-   Dell APEX Cloud Platform for Microsoft Azure Ansible Development Team &lt;<ansible.team@dell.com>&gt;