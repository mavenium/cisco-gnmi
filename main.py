from cisco_gnmi import ClientBuilder


def test():
    builder = ClientBuilder('37.156.144.182:57777')
    builder.set_os('IOS XR')
    builder.set_secure_from_file(
        root_certificates='rootCA.pem',
        private_key='rootCA.key',
        certificate_chain='client.crt',
    )
    builder.set_call_authentication('root', 'qbic@A9kDev2020')
    client = builder.construct()

    print(client.get_xpaths('/interfaces/interface'))


if __name__ == '__main__':
    test()
