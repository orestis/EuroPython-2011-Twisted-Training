from twisted.internet import reactor, protocol, defer


from simpleclient2 import gotData, UppercaseClientProtocol


if __name__ == '__main__':
    import sys
    host, port = sys.argv[1].split(':')
    data_to_send = sys.argv[2:]

    all_deferreds = []
    for data in data_to_send:
        print 'sending', data
        d = defer.Deferred()
        d.addCallback(gotData, data)
        factory = protocol.ClientFactory()
        factory.protocol = UppercaseClientProtocol
        factory.text = data
        factory.deferred = d
        all_deferreds.append(d)
        reactor.connectTCP(host, int(port), factory)

    deferredList = defer.DeferredList(all_deferreds)
    def all_done(results):
        reactor.stop()
    deferredList.addCallback(all_done)


    reactor.run()

