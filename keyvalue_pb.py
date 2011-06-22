from keyvalue import KeyValueStore
from twisted.internet import reactor
from twisted.spread import pb

class KeyValuePB(pb.Root):
    def __init__(self, store):
        self.store = store

    def remote_get(self, key):
        return self.store.get(key)

    def remote_set(self, key, value):
        return self.store.set(key, value)

    def remote_delete(self, key):
        return self.store.delete(key)

if __name__ == '__main__':
    from twisted.python import log
    import sys
    log.startLogging(sys.stdout)
    store = KeyValueStore()
    factory = pb.PBServerFactory(KeyValuePB(store))

    reactor.listenTCP(8789, factory)
    reactor.run()
