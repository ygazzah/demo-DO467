#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys

# Define the structure for the Ansible inventory
# This structure must conform to the dynamic inventory JSON output specification.
INVENTORY_DATA = {
    # Group for Windows servers
    "mywindows_servers": {
        "hosts": [
            "win1.example.com",
            "win2.example.com"
        ],
        # Group variables (optional, but good practice for Windows hosts)
        "vars": {
            "ansible_connection": "winrm",
            "ansible_port": 5986,
            "ansible_winrm_transport": "kerberos" # or 'ntlm'/'credssp'
        }
    },
    # Group for Linux servers
    "mylinux_servers": {
        "hosts": [
            "servera.example.com",
            "serverb.example.com"
        ],
        # Group variables (optional, default connection for Linux is 'ssh')
        "vars": {
            "ansible_user": "ec2-user", # Example user
            "ansible_port": 22
        }
    },
    # The _meta block is required by Ansible, even if empty, for host variables.
    "_meta": {
        "hostvars": {
            # You could add host-specific variables here if needed
            # "win1.example.com": { "some_variable": "value" }
        }
    }
}

def list_hosts():
    """Outputs the entire inventory when called without arguments."""
    return json.dumps(INVENTORY_DATA, indent=4)

def get_host_vars(hostname):
    """
    Returns variables specific to a single host.
    Since this script defines hosts statically, we only return _meta/hostvars.
    """
    return json.dumps(
        INVENTORY_DATA.get("_meta", {}).get("hostvars", {}).get(hostname, {}),
        indent=4
    )

if __name__ == '__main__':
    # Ansible expects the script to respond to two arguments: --list and --host
    if len(sys.argv) == 2 and sys.argv[1] == '--list':
        # Output the full inventory
        print(list_hosts())
    elif len(sys.argv) == 3 and sys.argv[1] == '--host':
        # Output host-specific variables (not used here, but required by API)
        hostname = sys.argv[2]
        print(get_host_vars(hostname))
    else:
        # Fallback for incorrect usage
        print(f"Usage: {sys.argv[0]} --list or {sys.argv[0]} --host <hostname>")
