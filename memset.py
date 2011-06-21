from twisted.internet import reactor, protocol, defer
from twisted.protocols import basic


class MemsetProtocol(basic.LineReceiver):

    def connectionMade(self):
        value = self.factory.value
        self.transport.write('set %s 0 0 %d\r\n' % (self.factory.key, len(value)))
        self.transport.write(value)
        self.transport.write('\r\n')


    def lineReceived(self, line):
        if line == 'STORED':
            self.factory.deferred.callback(self.factory.key)


if __name__ == '__main__':
    import sys
    host, port = sys.argv[1].split(':')
    key, value = sys.argv[2:]
    f = protocol.ClientFactory()
    f.protocol = MemsetProtocol
    f.key = key
    f.value = value
    f.deferred = defer.Deferred()
    reactor.connectTCP(host, int(port), f)
    f.deferred.addCallback(lambda _: reactor.stop())
    reactor.run()


