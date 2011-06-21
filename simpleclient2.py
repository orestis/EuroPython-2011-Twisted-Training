from twisted.internet import reactor, protocol, defer


class UppercaseClientProtocol(protocol.Protocol):
    def connectionMade(self):
        self.transport.write(self.factory.text)
        self.transport.write('\r\n')
        self.buffer = []

    def dataReceived(self, data):
        self.buffer.append(data)

    def connectionLost(self, reason):
        alldata = ''.join(self.buffer)
        self.factory.deferred.callback(alldata)


def gotData(data, request):
    print 'received response for', request
    print data


if __name__ == '__main__':
    import sys
    host, port = sys.argv[1].split(':')
    data_to_send = sys.argv[2:]

    for data in data_to_send:
        print 'sending', data
        d = defer.Deferred()
        d.addCallback(gotData, data)
        factory = protocol.ClientFactory()
        factory.protocol = UppercaseClientProtocol
        factory.text = data
        factory.deferred = d
        reactor.connectTCP(host, int(port), factory)

    reactor.run()

