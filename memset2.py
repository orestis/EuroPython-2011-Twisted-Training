from twisted.internet import reactor, protocol, defer
from twisted.python import failure
from twisted.protocols import basic


class MemsetProtocol(basic.LineReceiver):
    timedOut = False
    timeoutCall = None

    def connectionMade(self):
        value = self.factory.value
        self.transport.write('set %s 0 0 %d\r\n' % (self.factory.key, len(value)))
        self.transport.write(value)
        self.transport.write('\r\n')
        self.timeoutCall = reactor.callLater(self.factory.timeout, self.timeout)

    def timeout(self):
        self.factory.deferred.errback(failure.Failure(ValueError("Timeout")))
        self.timedOut = True


    def lineReceived(self, line):
        if self.timedOut:
            return
        if self.timeoutCall and self.timeoutCall.active():
            self.timeoutCall.cancel()
        if line == 'STORED':
            self.factory.deferred.callback(self.factory.key)
        elif line.startswith('CLIENT_ERROR'):
            _, msg = line.split(' ', 1)
            self.factory.deferred.errback(failure.Failure(ValueError(msg)))


if __name__ == '__main__':
    import sys
    host, port = sys.argv[1].split(':')
    key, value = sys.argv[2:]
    f = protocol.ClientFactory()
    f.protocol = MemsetProtocol
    f.timeout = 10
    f.key = key
    f.value = value
    f.deferred = defer.Deferred()
    reactor.connectTCP(host, int(port), f)
    f.deferred.addCallback(lambda _: reactor.stop())
    def err(f):
        print f.getErrorMessage()
        reactor.stop()
    f.deferred.addErrback(err)
    reactor.run()


