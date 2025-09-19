System Auto Discovery Hosts Module for APEX Cloud Platform Azure
=========================================
### Product Guide

> © 2023 Dell Inc. or its subsidiaries. All rights reserved. Dell 
> EMC, and other trademarks are trademarks of Dell Inc. or its 
> subsidiaries. Other trademarks may be trademarks of their respective owners.

Synopsis
--------
This module will get auto-discovered nodes before os provisioning.

Supported Endpoints
--------
* Get /system/initialize/nodes


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
            <div class="ansibleOptionAnchor" id="parameter-primary-host-ip"></div>
            <b>primary_host_ip</b>
            <a class="ansibleOptionLink" href="#parameter-primary-host-ip" title="Permalink to this option"></a>
            <div style="font-size: small">
                <span style="color: purple">type=string</span>
                <br>
                <span style="color: red">required=true</span>                    
            </div>
        </td>
        <td></td>
        <td>
            <div></div>
            <div>The ip address of primary host</div>
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
            <ul style="margin: 0; padding: 0"><b>Default</b>
                <li>60s</li>
            </ul>
        </td>
        <td>
            <div></div>
            <div>Time out value for get auto-discovered nodes, the default value is 60 seconds</div>
            <div></div>
        </td>
    </tr>
</table>

Notes
-----
- Make sure your Apex Cloud Platform environment supports the API that you use
- Details on execution of module dell_apexcp_azure_auto_discovery_hosts.py can be checked in the logs /tmp/apexcp_azure_auto_discovery_host.log

Examples
--------

``` yaml+jinja
    - name: Get Auto-discovered Nodes before os provisioning 
      dellemc.apexcp_azure.dell_apexcp_azure_auto_discovery_hosts:
        primary_host_ip: "{{ primary_host_ip }}"
```

Return Values
-------------

The following are the fields unique to this module:

Return Values
-------------

The following are the fields unique to this module:

<table border=0 cellpadding=0 class="documentation-table">
    <tr>
        <th colspan="3">Key</th>
        <th>Returned</th>
        <th width="100%">Description</th>
    </tr>
    <tr>
        <td colspan="3">
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
        <td colspan="3">
            <div class="ansibleOptionAnchor" id="return-System-Initialize-Nodes-Information"></div>
            <b>System_Initialize_Nodes_Information</b>
            <a class="ansibleOptionLink" href="#return-System-Initialize-Nodes-Information" title="Permalink to this return value"></a>
            <div style="font-size: small"><span style="color: purple">type=dictionary</span></div>
        </td>
        <td>When calling the /system/initialize/nodes API is successful</td>
        <td><div>Information of discovered node</div><br/></td>
    </tr>
    <tr>
        <td class="elbow-placeholder">&nbsp;</td>
        <td colspan="2">
            <div class="ansibleOptionAnchor" id="return-nodes-info/auto-discovered-node-sort"></div>
            <b>auto_discovered_node_sort</b>
            <a class="ansibleOptionLink" href="#return-nodes-info/auto-discovered-node-sort" title="Permalink to this return value"></a>
            <div style="font-size: small"><span style="color: purple">type=dictionary</span></div>
        </td>
        <td>success</td>
        <td>
            <div>auto discovered node sort name</div>
        </td>
    </tr>
    <tr>
        <td class="elbow-placeholder">&nbsp;</td>
        <td class="elbow-placeholder">&nbsp;</td>
        <td colspan="1">
            <div class="ansibleOptionAnchor" id="return-nodes-info/auto-discovered-node-sort/bootstrap-os-version"></div>
            <b>bootstrap_os_version</b>
            <a class="ansibleOptionLink" href="#return-nodes-info/auto-discovered-node-sort/bootstrap-os-version" title="Permalink to this return value"></a>
            <div style="font-size: small"><span style="color: purple">type=string</span></div>
        </td>
        <td></td>
        <td><div>The version of bootstrap OS installed on the host</div></td>
    </tr>
    <tr>
        <td class="elbow-placeholder">&nbsp;</td>
        <td class="elbow-placeholder">&nbsp;</td>
        <td colspan="1">
            <div class="ansibleOptionAnchor" id="return-nodes-info/auto-discovered-node-sort/hostname"></div>
            <b>hostname</b>
            <a class="ansibleOptionLink" href="#return-nodes-info/auto-discovered-node-sort/hostname" title="Permalink to this return value"></a>
            <div style="font-size: small"><span style="color: purple">type=string</span></div>
        </td>
        <td></td>
        <td><div>The hostname of the host</div></td>
    </tr>
    <tr>
        <td class="elbow-placeholder">&nbsp;</td>
        <td class="elbow-placeholder">&nbsp;</td>
        <td colspan="1">
            <div class="ansibleOptionAnchor" id="return-nodes-info/auto-discovered-node-sort/ipv6"></div>
            <b>ipv6</b>
            <a class="ansibleOptionLink" href="#return-nodes-info/auto-discovered-node-sort/ipv6" title="Permalink to this return value"></a>
            <div style="font-size: small"><span style="color: purple">type=string</span></div>
        </td>
        <td></td>
        <td><div>The IPv6 address of the host</div></td>
    </tr>
    <tr>
        <td class="elbow-placeholder">&nbsp;</td>
        <td class="elbow-placeholder">&nbsp;</td>
        <td colspan="1">
            <div class="ansibleOptionAnchor" id="return-nodes-info/auto-discovered-node-sort/model"></div>
            <b>model</b>
            <a class="ansibleOptionLink" href="#return-nodes-info/auto-discovered-node-sort/model" title="Permalink to this return value"></a>
            <div style="font-size: small"><span style="color: purple">type=string</span></div>
        </td>
        <td></td>
        <td><div>The model of the host</div></td>
    </tr>
    <tr>
        <td class="elbow-placeholder">&nbsp;</td>
        <td class="elbow-placeholder">&nbsp;</td>
        <td colspan="1">
            <div class="ansibleOptionAnchor" id="return-nodes-info/auto-discovered-node-sort/primary"></div>
            <b>primary</b>
            <a class="ansibleOptionLink" href="#return-nodes-info/auto-discovered-node-sort/primary" title="Permalink to this return value"></a>
            <div style="font-size: small"><span style="color: purple">type=boolean</span></div>
        </td>
        <td></td>
        <td><div>Indicate whether the host is primary or not</div></td>
    </tr>
    <tr>
        <td class="elbow-placeholder">&nbsp;</td>
        <td class="elbow-placeholder">&nbsp;</td>
        <td colspan="1">
            <div class="ansibleOptionAnchor" id="return-nodes-info/auto-discovered-node-sort/serial-number"></div>
            <b>serial_number</b>
            <a class="ansibleOptionLink" href="#return-nodes-info/auto-discovered-node-sort/serial-number" title="Permalink to this return value"></a>
            <div style="font-size: small"><span style="color: purple">type=string</span></div>
        </td>
        <td></td>
        <td><div>The service tag of the node</div></td>
    </tr>
    <tr>
        <td colspan="3">
            <div class="ansibleOptionAnchor" id="return-msg"></div>
            <b>msg</b>
            <a class="ansibleOptionLink" href="#return-msg" title="Permalink to this return value"></a>
            <div style="font-size: small"><span style="color: purple">type=string</span></div>
        </td>
        <td>Always</td>
        <td><div>The message of get auto-discovered nodes</div></td>
    </tr>
</table>

Authors
-------

-   Dell APEX Cloud Platform for Microsoft Azure Ansible Development Team &lt;<ansible.team@dell.com>&gt;