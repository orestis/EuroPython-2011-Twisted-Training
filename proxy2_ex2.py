from twisted.web.client import getPage
from twisted.internet import reactor, protocol, defer
from twisted.protocols import basic

class CachingProxyProtocol(basic.LineReceiver):

    def _getPage(self, url):
        try:
            data = self.factory.cache[url]
            return defer.succeed(data)
        except KeyError:
            d = getPage(url)
            d.addCallback(self._storeInCache, url, self.factory.cache)
            return d

    def _storeInCache(self, data, url, cache):
        cache[url] = data
        return data

    def writeDataToTransport(self, data):
        self.transport.write(data)
        self.transport.loseConnection()

    def lineReceived(self, line):
        if not line.startswith('http://'):
            return
        deferredData = self._getPage(line)
        deferredData.addCallback(self.writeDataToTransport)

class CachingProxyFactory(protocol.ServerFactory):
    protocol = CachingProxyProtocol
    cache = {}

reactor.listenTCP(8000, CachingProxyFactory())
reactor.run()


