Cluster Deployment Module for APEX Cloud Platform Azure
=================
### Product Guide

> © 2023 Dell Inc. or its subsidiaries. All rights reserved. Dell 
> EMC, and other trademarks are trademarks of Dell Inc. or its 
> subsidiaries. Other trademarks may be trademarks of their respective owners. 

Synopsis
--------
This module will configure and deploy a new APEX Cloud Platform 
cluster for Microsoft Azure based on the provided day1 json file.
  
Supported Endpoints
--------

* POST /system/initialize?mode=CLUSTER_DEPLOYMENT
* GET /system/initialize/status?mode=CLUSTER_DEPLOYMENT  

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
            <div>The path of day1 json file</div>
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
        <td>
            <ul style="margin: 0; padding: 0"><b>Default:</b>
                <li>36000s</li>
            </ul>
        </td>
        <td>
            <div></div>
            <div>Time out value for performing cluster deployment, the default value is 36000 seconds</div>
            <div></div>
        </td>
    </tr>
</table>

Notes
-----
- Make sure your APEX Cloud Platform Azure environment supports the API that you use
- Please check "Chapter 4:Prerequisites" of "Deployment Guide" to prepare system prerequisites before perform module.
- Details on execution of module dell_apexcp_azure_cluster_deployment.py can be checked in the logs /tmp/apexcp_azure_cluster_deployment.log


Examples
--------

``` yaml+jinja
  - name: Configure and deploy a new APEX Cloud Platform cluster for Azure
    dell_apexcp_azure_cluster_deployment:
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
        <td>Always</td>
        <td>
            <div>Whether or not the resource has changed.</div><br/>
        </td>
    </tr>
    <tr>
        <td colspan="2">
            <div class="ansibleOptionAnchor" id="return-day1-initialization"></div>
            <b>cluster_deployment_result</b>
            <a class="ansibleOptionLink" href="#return-day1-initialization" title="Permalink to this return value"></a>
            <div style="font-size: small"><span style="color: purple">type=dict</span></div>
        </td>
        <td>When calling the /system/initialize?mode=CLUSTER_DEPLOYMENT API is successful</td>
        <td><div></div><br/></td>
    </tr>
    <tr>
        <td class="elbow-placeholder">&nbsp;</td>
        <td colspan="1">
            <div class="ansibleOptionAnchor" id="return-install-status/request-id"></div>
            <b>request_id</b>
            <a class="ansibleOptionLink" href="#return-install-status/request-id" title="Permalink to this return value"></a>
            <div style="font-size: small"><span style="color: purple">type=string</span></div>
        </td>
        <td></td>
        <td>
            <div>The request id of cluster deployment.</div>
        </td>
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
        <td><div>The cluster deployment result.</div></td>
    </tr>
    <tr>
        <td colspan="2">
            <div class="ansibleOptionAnchor" id="return-msg"></div>
            <b>msg</b>
            <a class="ansibleOptionLink" href="#return-msg" title="Permalink to this return value"></a>
            <div style="font-size: small"><span style="color: purple">type=string</span></div>
        </td>
        <td>Always</td>
        <td><div>The message for cluster deployment</div></td>
    </tr>
</table>

Authors
-------

-   Dell APEX Cloud Platform for Microsoft Azure Ansible Development Team &lt;<ansible.team@dell.com>&gt;