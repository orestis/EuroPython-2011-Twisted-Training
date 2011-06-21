from twisted.web.client import getPage
from twisted.internet import reactor, protocol, defer
from twisted.protocols import basic



class CachingProxyProtocol(basic.LineReceiver):

    def _getPage(self, url, cache):
        try:
            data = self.factory.cache[url]
            return defer.succeed(data)
        except KeyError:
            d = getPage(url)
            d.addCallback(self._storeInCache, url, cache)
            return d


    def _storeInCache(self, data, url, cache):
        cache[url] = data
        return data


    def lineReceived(self, line):
        if not line.startswith('http://'):
            return
        def gotData(data):
            self.transport.write(data)
            self.transport.loseConnection()
        deferredData = self._getPage(line, self.factory.cache)
        deferredData.addCallback(gotData)


class CachingProxyFactory(protocol.ServerFactory):
    protocol = CachingProxyProtocol
    cache = {}

reactor.listenTCP(8000, CachingProxyFactory())
reactor.run()


