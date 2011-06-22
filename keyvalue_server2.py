from keyvalue import KeyValueStore
from keyvalue_server import KeyValueStoreProtocol
from keyvalue_pb import KeyValuePB
from twisted.spread import pb

from twisted.internet import reactor, protocol


if __name__ == '__main__':
    from twisted.python import log
    import sys
    log.startLogging(sys.stdout)
    store = KeyValueStore()

    factory = protocol.ServerFactory()
    factory.protocol = KeyValueStoreProtocol
    factory.store = store
    reactor.listenTCP(11211, factory)

    pb_factory = pb.PBServerFactory(KeyValuePB(store))
    reactor.listenTCP(8789, pb_factory)

    reactor.run()
                

