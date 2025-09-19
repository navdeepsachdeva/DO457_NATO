Role Name
=========

mfitbs_openvpn_server

Requirements
------------

* Ansible 2.8.5
* Debian 10
* Debian 9

Role Variables
--------------

###### EasyRSA host
* easy_rsa_host - host on which easyrsa will be installed.

###### Server host
* server_port - Openvpn server/hub port.
* client_to_client - is client to client communication allowed.

###### all
* id_type - ID type (certficate field subject-alt-name) in cert can be DNS or IP
* proto - proto for openvpm connections values:tcp,udp 
* host_pki_dir - host PKI dir (where keys, certs, ... being kept).
* dh_len - Diffie–Hellman param length. 
* cipher - openvpn cipher.
* log_status - openvpn status log.
* log - openvpn log. 

Dependencies
------------

* mfitbs-openvpn-easyrsa

Example Playbook
----------------

* inventory


    erh ansible_host=192.168.51.5 ansible_user=root ansible_password=qwerty ansible_ssh_common_args='-o StrictHostKeyChecking=no'
    
    [server]
    server ansible_host=192.168.51.4 ansible_user=root ansible_password=qwerty ansible_ssh_common_args='-o StrictHostKeyChecking=no'
    
    [client]
    client1 ansible_host=192.168.51.6 client_addr=10.8.0.2 client_mask=255.255.255.0 ansible_user=root ansible_password=qwerty ansible_ssh_common_args='-o StrictHostKeyChecking=no'


* playbook


    - name: Test server part
      hosts: server
      roles:
        - role: mfitbs-openvpn-server
          vars:
            server_port: 1194
            proto: tcp
            log_status: /var/log/openvpn-status.log
            log: /var/log/openvpn.log
            host_pki_dir: /etc/pki/openvpn
            cipher: AES-256-CBC
            id_type: IP
            easy_rsa_host: erh
            client_to_client: true
      tasks:


License
-------

MIT

Author Information
------------------

Marcin Faryna
