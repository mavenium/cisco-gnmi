from cisco_gnmi import ClientBuilder
import re
import json


def test():
    builder = ClientBuilder('37.156.144.182:57777')
    builder.set_os('IOS XR')
    builder.set_secure_from_target()
    builder.set_ssl_target_override()
    builder.set_call_authentication('root', 'qbic@A9kDev2020')
    client = builder.construct()

    result = client.get_xpaths('/interfaces/interface', data_type="ALL", encoding="JSON_IETF")

    interfaces = []
    for interface in json.loads(re.findall('(?<=json_ietf_val: ")(.*)(?=")', str(result))[0].replace('\\\"', "\"")):
        if not any(item in interface['name'] for item in ['Null', 'SINT']):
            if 'config' in interface:
                if 'enabled' in interface['config']:
                    del interface['config']['enabled']

            if 'state' in interface:
                del interface['state']['ifindex']
                del interface['state']['admin-status']
                del interface['state']['oper-status']
                del interface['state']['last-change']
                del interface['state']['logical']
                del interface['state']['loopback-mode']
                del interface['state']['type']
                del interface['state']['enabled']

                if 'counters' in interface['state']:
                    del interface['state']['counters']

            if 'subinterfaces' in interface:
                for subinterface in interface['subinterfaces']['subinterface']:

                    if 'config' in subinterface:
                        if 'index' in subinterface['config']:
                            del subinterface['config']['index']

                    if 'state' in subinterface:
                        del subinterface['state']

                    if 'index' in subinterface:
                        del subinterface['index']

                    if 'openconfig-if-ip:ipv4' in subinterface:
                        if 'state' in subinterface['openconfig-if-ip:ipv4']:
                            del subinterface['openconfig-if-ip:ipv4']['state']

                        if 'neighbors' in subinterface['openconfig-if-ip:ipv4']:
                            del subinterface['openconfig-if-ip:ipv4']['neighbors']

                        if 'addresses' in subinterface['openconfig-if-ip:ipv4']:
                            for address in subinterface['openconfig-if-ip:ipv4']['addresses']['address']:
                                if 'state' in address:
                                    del address['state']

                    if 'openconfig-if-ip:ipv6' in subinterface:
                        if 'state' in subinterface['openconfig-if-ip:ipv6']:
                            del subinterface['openconfig-if-ip:ipv6']['state']

                        if 'neighbors' in subinterface['openconfig-if-ip:ipv6']:
                            del subinterface['openconfig-if-ip:ipv6']['neighbors']

                        if 'addresses' in subinterface['openconfig-if-ip:ipv6']:
                            for address in subinterface['openconfig-if-ip:ipv6']['addresses']['address']:
                                if 'state' in address:
                                    del address['state']

                    if 'openconfig-vlan:vlan' in subinterface:
                        del subinterface['openconfig-vlan:vlan']

            if 'openconfig-if-aggregate:aggregation' in interface:
                del interface['openconfig-if-aggregate:aggregation']

            if 'openconfig-if-ethernet:ethernet' in interface:
                del interface['openconfig-if-ethernet:ethernet']

            interfaces.append(interface)

    # print(interfaces)

    openconfig_interfaces = str({
        'openconfig-interfaces:interfaces': {
            'interface': interfaces
        }
    }).replace("'", '"').replace('True', '"True"').replace('False', '"False"')

    print(openconfig_interfaces)

    try:
        # config = '{"openconfig-interfaces:interfaces": {"interface": [{"name": "Loopback70", "config": {"name": "Loopback70"}, "subinterfaces": {"subinterface": [{"index": 0, "openconfig-if-ip:ipv4": {"addresses": {"address": [{"ip": "192.0.2.255", "config": {"ip": "192.0.2.255", "prefix-length": 32}}]}}, "openconfig-if-ip:ipv6": {"addresses": {"address": [{"ip": "2001:db8::100", "config": {"ip": "2001:db8::100", "prefix-length": 128}}]}}}]}}]}}'
        set_response = client.set_json(replace_json_configs=openconfig_interfaces)
        print(set_response)
    except Exception as e:
        print(e)

    # bgps = client.get_xpaths('/bgp-cfg/bgp', data_type="ALL", encoding="JSON_IETF")
    # print(bgps)


if __name__ == '__main__':
    test()
