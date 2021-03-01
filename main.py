from cisco_gnmi import ClientBuilder


def test():
    builder = ClientBuilder('64.103.37.3:19399')
    builder.set_os('IOS XR')
    builder.set_secure_from_target()
    builder.set_call_authentication('admin', 'C1sco12345')
    client = builder.construct()

    print(client.get_xpaths('interfaces/interface'))


if __name__ == '__main__':
    test()
