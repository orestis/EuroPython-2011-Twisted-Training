from keyvalue import KeyValueStore

from twisted.internet import reactor, protocol
from twisted.protocols import basic


class KeyValueStoreProtocol(basic.LineReceiver):
    def lineReceived(self, line):
        print 'R', line
        command, args = line.split()[0], line.split()[1:]
        if command == 'get':
            try:
                value = self.factory.store.get(args[0])
                self.sendLine('VALUE %s %s' % (args[0], value))
            except KeyError:
                self.sendLine('GET_NOT_FOUND %s' % args[0])
        elif command == 'set':
            self.factory.store.set(args[0], args[1])
            self.sendLine('STORED')
        elif command == 'delete':
            try:
                self.factory.store.delete(args[0])
                self.sendLine('DELETED %s' % args[0])
            except KeyError:
                self.sendLine('DEL_NOT_FOUND %s' % args[0])

if __name__ == '__main__':
    from twisted.python import log
    import sys
    log.startLogging(sys.stdout)
    factory = protocol.ServerFactory()
    factory.protocol = KeyValueStoreProtocol
    factory.store = KeyValueStore()

    reactor.listenTCP(11211, factory)
    reactor.run()
                

