from twisted.internet import reactor, protocol, defer
from twisted.protocols import basic

class MemcacheGetProtocol(basic.LineReceiver):

    def connectionMade(self):
        self.buffer = []
        self.length = None
        self.value = None
        self.transport.write('get %s\r\n' % (self.factory.key,))


    def lineReceived(self, line):
        if line.startswith('VALUE %s' % self.factory.key):
            length = int(line.rsplit(' ', 1)[-1])
            self.length = length
            self.setRawMode()
        if line == 'END':
            self.factory.deferred.callback(self.value)


    def rawDataReceived(self, data):
        self.buffer.append(data)
        raw = ''.join(self.buffer)
        if len(raw) >= self.length:
            self.value = raw[:self.length]
            rest = raw[self.length:]
            self.setLineMode(rest)

if __name__ == '__main__':
    import sys
    host, port = sys.argv[1].split(':')
    key = sys.argv[2]
    f = protocol.ClientFactory()
    f.protocol = MemcacheGetProtocol
    f.key = key
    f.deferred = defer.Deferred()
    reactor.connectTCP(host, int(port), f)
    def gotData(d):
        print d
        reactor.stop()
    f.deferred.addCallback(gotData)
    reactor.run()


