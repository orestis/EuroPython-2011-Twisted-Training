from twisted.internet import reactor, protocol


class UpperProtocol(protocol.Protocol):

    def connectionMade(self):
        self.factory.count += 1
        self.transport.write('Hi! There are %d clients\n' % self.factory.count)

    def connectionLost(self, reason):
        self.factory.count -= 1

    def dataReceived(self, data):
        self.transport.write(data.upper())
        self.transport.loseConnection()

class CountingFactory(protocol.ServerFactory):
    protocol = UpperProtocol
    count = 0

reactor.listenTCP(8000, CountingFactory())

reactor.run()

