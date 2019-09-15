#!/usr/bin/env python3
from time import sleep
from os import listdir
from fcntl import ioctl
from struct import pack

import socket

from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily


def get_all():
    interfaces = [Interface(name) for name in listdir('/sys/class/net/')]
    return interfaces


class Interface:
    """
    An interface object with attributes name, ip_address and status.
    Status check is based on values from /sys/class/net. May be:
    1 - if operstate is 'up'. Else if operstate is 'unknown' and carrier is 1. It's made
        for virtual drivers like TUN/TAP or if driver doesn't support/show operstate
    0 - in other cases
    """
    def __init__(self, name):
        self.name = name
        self._operstate = self._get_operstate()
        self._carrier = self._get_carrier()
        self.ip_address = self._get_ip()
        self.status = self._get_status()

    def _get_operstate(self):
        try:
            with open('/sys/class/net/{}/operstate'.format(self.name), 'r') as operstate:
                return operstate.read().rstrip()
        except (FileNotFoundError, OSError):
            return None

    def _get_carrier(self):
        try:
            with open('/sys/class/net/{}/carrier'.format(self.name), 'r') as carrier:
                return carrier.read().rstrip()
        except (FileNotFoundError, OSError):
            return None

    def _get_ip(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            return socket.inet_ntoa(ioctl(
                sock.fileno(),
                0x8915,  # SIOCGIFADDR
                pack('256s', self.name[:15].encode('utf-8'))
            )[20:24])
        except OSError:
            return ''

    def _get_status(self):
        if self._operstate == 'up':
            return 1
        if self._operstate == 'unknown' and self._carrier == '1':
            return 1
        return 0


class InterfaceCollector:
    """
    Custom collector for check interfaces statuses
    """
    def collect(self):
        metric = GaugeMetricFamily('interface_status',
                                   'Value is 1.0 if interface active, 0.0 - inactive',
                                   labels=['address', 'name'])
        for interface in get_all():
            metric.add_metric([interface.ip_address, interface.name], interface.status)
        yield metric


if __name__ == '__main__':
    start_http_server(8220, registry=InterfaceCollector())
    while True:
        sleep(1)
