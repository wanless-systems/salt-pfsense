# -*- coding: utf-8 -*-
"""
Module for running pfsense module via fauxapi
"""
from __future__ import absolute_import

# Import Python libs
import os
import re
import base64
import hashlib
import time
import binascii
import logging
import json

# Import Salt libs
import salt.utils.files
import salt.utils.stringutils
import pfsense
from salt.exceptions import (
    CommandExecutionError,
    SaltInvocationError,
)

# Import 3rd-party libs
from salt.ext import six
from salt.ext.six.moves import range

logger = logging.getLogger(__name__)

def __virtual__():
    if os.path.isfile('/etc/pf.os'):
        return True
    else:
        return False

def _get_client():
    return pfsense.FauxapiLib(debug=True)


def list_servers(all_data=False):
    """Return dict of crls."""
    client = _get_client()
    config = client.config_get()

    ret = {}
    if 'openvpn' not in config:
        return ret

    config = config['openvpn']
    if 'openvpn-server' not in config:
        return ret

    for server in config['openvpn-server']:
        vpnid = int(server['vpnid'])
        if all_data:
            data = server
        else:
            data = {
                'vpnid': vpnid,
                'description': server['description'],
                'caref': server['caref'],
                'mode': server['mode'],
                'protocol': server['protocol'],
                'dev_mode': server['dev_mode'],
                'interface': server['interface'],
                'local_port': server['local_port'],
            }
            if 'auth_mode' in server:
                data['auth_mode'] = server['auth_mode']
        ret[vpnid] = data
    return ret


def get_server(vpnid, all_data=False):
    """Return specific server."""
    vpnid = int(vpnid)
    servers = list_servers(all_data)
    logger.warning('test')
    logger.warning(servers)
    logger.warning(vpnid)
    if str(vpnid) not in servers:
        return None
    return servers[vpnid]
