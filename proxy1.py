from twisted.internet import reactor, protocol
from twisted.protocols import basic

import urllib2
import time


class ProxyProtocol(basic.LineReceiver):

    def lineReceived(self, line):
        if not line.startswith('http://'):
            return
        start = time.time()
        print 'fetching', line
        data = urllib2.urlopen(line).read()
        print 'fetched', line
        self.transport.write(data)
        self.transport.loseConnection()
        print 'took', time.time() - start

factory = protocol.ServerFactory()
factory.protocol = ProxyProtocol

reactor.listenTCP(8000, factory)
reactor.run()


