from twisted.internet import reactor, protocol, defer

import time

from simpleclient2 import UppercaseClientProtocol

def gotData(data, request, starttime):
    print 'request', request, 'took', time.time() - starttime
    return (request, data)

if __name__ == '__main__':
    import sys
    host, port = sys.argv[1].split(':')
    data_to_send = sys.argv[2:]

    overallstart = time.time()
    all_deferreds = []
    for data in data_to_send:
        print 'sending', data
        d = defer.Deferred()
        d.addCallback(gotData, data, time.time())
        factory = protocol.ClientFactory()
        factory.protocol = UppercaseClientProtocol
        factory.text = data
        factory.deferred = d
        all_deferreds.append(d)
        reactor.connectTCP(host, int(port), factory)

    deferredList = defer.DeferredList(all_deferreds)
    def all_done(results):
        for success, result in results:
            print result
        reactor.stop()
    deferredList.addCallback(all_done)


    reactor.run()
    print 'finished, took', time.time() - overallstart
