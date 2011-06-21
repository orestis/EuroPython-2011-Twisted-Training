from twisted.internet import reactor, protocol


class UppercaseClientProtocol(protocol.Protocol):
    def connectionMade(self):
        self.transport.write(self.factory.text)
        self.transport.write('\r\n')

    def dataReceived(self, data):
        print data


if __name__ == '__main__':
    import sys
    host, port = sys.argv[1].split(':')
    data_to_send = sys.argv[2:]

    for d in data_to_send:
        print 'sending', d
        factory = protocol.ClientFactory()
        factory.protocol = UppercaseClientProtocol
        factory.text = d
        reactor.connectTCP(host, int(port), factory)

    reactor.run()
