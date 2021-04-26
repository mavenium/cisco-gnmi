from cisco_gnmi import ClientBuilder
import re
import json
from os import environ
from dotenv import load_dotenv, find_dotenv


def get_interfaces():
    load_dotenv(find_dotenv())

    builder = ClientBuilder('{0}:{1}'.format(environ.get("ROUTER_IP"), environ.get("ROUTER_PORT")))
    builder.set_os('IOS XR')
    builder.set_secure_from_target()
    builder.set_ssl_target_override()
    builder.set_call_authentication(environ.get("ROUTER_USER"), environ.get("ROUTER_PASSWORD"))
    client = builder.construct()

    result = client.get_xpaths('/interfaces/interface', data_type="ALL", encoding="JSON_IETF")

    interfaces = []
    for interface in json.loads(re.findall('(?<=json_ietf_val: ")(.*)(?=")', str(result))[0].replace('\\\"', "\"")):
        if not any(item in interface['name'] for item in ['Null', 'SINT']):
            interface_item = {}

            if 'name' in interface:
                interface_item['name'] = interface['name']

            interface_item['description'] = ''

            if 'config' in interface and 'mtu' in interface['config']:
                interface_item['mtu'] = interface['config']['mtu']
            elif 'state' in interface and 'mtu' in interface['state']:
                interface_item['mtu'] = interface['state']['mtu']

            if 'subinterfaces' in interface:
                interface_item['addresses'] = {}

                for subinterface in interface['subinterfaces']['subinterface']:

                    if 'openconfig-if-ip:ipv4' in subinterface:
                        if 'addresses' in subinterface['openconfig-if-ip:ipv4']:
                            ipv4 = []
                            for address in subinterface['openconfig-if-ip:ipv4']['addresses']['address']:
                                ipv4.append(address['config'])
                            interface_item['addresses']['ipv4'] = ipv4

                    if 'openconfig-if-ip:ipv6' in subinterface:
                        if 'addresses' in subinterface['openconfig-if-ip:ipv6']:
                            ipv6 = []
                            for address in subinterface['openconfig-if-ip:ipv6']['addresses']['address']:
                                ipv6.append(address['config'])
                            interface_item['addresses']['ipv6'] = ipv6

                    if len(interface_item['addresses']) == 0:
                        del interface_item['addresses']

            interfaces.append(interface_item)

    openconfig_interfaces = str({
        'openconfig-interfaces:interfaces': {
            'interface': interfaces
        }
    }).replace("'", '"')

    print(openconfig_interfaces)

    # test = '{"openconfig-interfaces:interfaces": {"interface": [{"name": "Loopback70", "config": {"name": "Loopback70"}, "subinterfaces": {"subinterface": [{"index": 0, "openconfig-if-ip:ipv4": {"addresses": {"address": [{"ip": "99.99.99.99", "config": {"ip": "99.99.99.99", "prefix-length": 24}}, {"ip": "1.1.1.1", "config": {"ip": "1.1.1.1", "prefix-length": 30}}, {"ip": "192.0.2.255", "config": {"ip": "192.0.2.255", "prefix-length": 32}}]}}, "openconfig-if-ip:ipv6": {"addresses": {"address": [{"ip": "2001:db8::100", "config": {"ip": "2001:db8::100", "prefix-length": 128}}]}}}]}}, {"name": "Bundle-Ether300", "config": {"name": "Bundle-Ether300"}, "subinterfaces": {"subinterface": [{"index": 20, "config": {}, "openconfig-if-ip:ipv4": {"addresses": {"address": [{"ip": "192.0.2.4", "config": {"ip": "192.0.2.4", "prefix-length": 31}}]}}, "openconfig-if-ip:ipv6": {"addresses": {"address": [{"ip": "2001::db8:1000:1000:b", "config": {"ip": "2001::db8:1000:1000:b", "prefix-length": 127}}]}}}, {"index": 0, "openconfig-if-ip:ipv4": {}, "openconfig-if-ip:ipv6": {}}]}}, {"name": "Bundle-Ether5000", "config": {"name": "Bundle-Ether5000", "mtu": 9000}, "subinterfaces": {"subinterface": [{"index": 0, "openconfig-if-ip:ipv4": {"addresses": {"address": [{"ip": "192.0.2.0", "config": {"ip": "192.0.2.0", "prefix-length": 31}}]}}, "openconfig-if-ip:ipv6": {"addresses": {"address": [{"ip": "2001:db8:10::a", "config": {"ip": "2001:db8:10::a", "prefix-length": 127}}]}}}]}}, {"name": "GigabitEthernet0/0/0/0", "config": {"name": "GigabitEthernet0/0/0/0"}, "subinterfaces": {"subinterface": [{"index": 0, "openconfig-if-ip:ipv4": {"addresses": {"address": [{"ip": "37.156.144.182", "config": {"ip": "37.156.144.182", "prefix-length": 28}}]}}, "openconfig-if-ip:ipv6": {}}]}}, {"name": "GigabitEthernet0/0/0/1", "config": {"name": "GigabitEthernet0/0/0/1", "mtu": 9000}, "subinterfaces": {"subinterface": [{"index": 0, "openconfig-if-ip:ipv4": {"addresses": {"address": [{"ip": "192.168.10.1", "config": {"ip": "192.168.10.1", "prefix-length": 24}}]}}, "openconfig-if-ip:ipv6": {}}]}}, {"name": "GigabitEthernet0/0/0/2", "config": {"name": "GigabitEthernet0/0/0/2"}, "subinterfaces": {"subinterface": [{"index": 0, "openconfig-if-ip:ipv4": {"addresses": {"address": [{"ip": "192.168.20.1", "config": {"ip": "192.168.20.1", "prefix-length": 24}}]}}, "openconfig-if-ip:ipv6": {"addresses": {"address": [{"ip": "2001:db8:20::1", "config": {"ip": "2001:db8:20::1", "prefix-length": 64}}]}}}]}}, {"name": "GigabitEthernet0/0/0/4", "config": {"name": "GigabitEthernet0/0/0/4", "mtu": 9000}, "subinterfaces": {"subinterface": [{"index": 10, "config": {}, "openconfig-if-ip:ipv4": {"addresses": {"address": [{"ip": "192.0.2.2", "config": {"ip": "192.0.2.2", "prefix-length": 31}}]}}, "openconfig-if-ip:ipv6": {"addresses": {"address": [{"ip": "2001:db8:20::a", "config": {"ip": "2001:db8:20::a", "prefix-length": 127}}]}}}, {"index": 0, "openconfig-if-ip:ipv4": {}, "openconfig-if-ip:ipv6": {}}]}}, {"name": "GigabitEthernet0/0/0/3", "subinterfaces": {"subinterface": [{"index": 0, "openconfig-if-ip:ipv4": {}, "openconfig-if-ip:ipv6": {}}]}}, {"name": "GigabitEthernet0/0/0/5", "subinterfaces": {"subinterface": [{"index": 0, "openconfig-if-ip:ipv4": {}, "openconfig-if-ip:ipv6": {}}]}}, {"name": "GigabitEthernet0/0/0/6", "subinterfaces": {"subinterface": [{"index": 0, "openconfig-if-ip:ipv4": {}, "openconfig-if-ip:ipv6": {}}]}}, {"name": "MgmtEth0/RP0/CPU0/0", "subinterfaces": {"subinterface": [{"index": 0, "openconfig-if-ip:ipv4": {}, "openconfig-if-ip:ipv6": {}}]}}]}}'
    #
    # try:
    #     config = '{"openconfig-interfaces:interfaces": {"interface": [{"name": "Loopback70", "config": {"name": "Loopback70"}, "subinterfaces": {"subinterface": [{"index": 0, "openconfig-if-ip:ipv4": {"addresses": {"address": [{"ip": "192.0.2.255", "config": {"ip": "192.0.2.255", "prefix-length": 32}}]}}, "openconfig-if-ip:ipv6": {"addresses": {"address": [{"ip": "2001:db8::100", "config": {"ip": "2001:db8::100", "prefix-length": 128}}]}}}]}}]}}'
    #     set_response = client.set_json(update_json_configs=openconfig_interfaces)
    #     print(set_response)
    # except Exception as e:
    #     print(e)


def get_bgp():
    load_dotenv(find_dotenv())

    builder = ClientBuilder('{0}:{1}'.format(environ.get("ROUTER_IP"), environ.get("ROUTER_PORT")))
    builder.set_os('IOS XR')
    builder.set_secure_from_target()
    builder.set_ssl_target_override()
    builder.set_call_authentication(environ.get("ROUTER_USER"), environ.get("ROUTER_PASSWORD"))
    client = builder.construct()

    result = client.get_xpaths(xpaths='/oc-bgp/')

    print(result)


def get_cli():
    load_dotenv(find_dotenv())

    builder = ClientBuilder('{0}:{1}'.format(environ.get("ROUTER_IP"), environ.get("ROUTER_PORT")))
    builder.set_os('IOS XR')
    builder.set_secure_from_target()
    builder.set_ssl_target_override()
    builder.set_call_authentication(environ.get("ROUTER_USER"), environ.get("ROUTER_PASSWORD"))
    client = builder.construct()

    result = client.get_cli('show run router bgp')

    print(result)


if __name__ == '__main__':
    # get_interfaces()
    # get_bgp()
    get_cli()
