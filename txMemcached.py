from twisted.internet import reactor, protocol, defer
from twisted.protocols import basic

class MemcacheProtocol(basic.LineReceiver):
    def __init__(self):
        self.requests = []
        self.lock = defer.DeferredLock()
        self.connectedDeferred = defer.Deferred()


    def connectionMade(self):
        self.connectedDeferred.callback(self)


    def set(self, key, value):
        d = defer.Deferred()
        request = (d, key, value)
        self.requests.insert(0, request)
        self.lock.acquire().addCallback(self._do_set, key, value)
        return d

    def _do_set(self, lock, key, value):
        self.transport.write('set %s 0 0 %d\r\n' % (key, len(value)))
        self.transport.write(value)
        self.transport.write('\r\n')


    def get(self, key):
        d = defer.Deferred()
        request = (d, key)
        self.requests.insert(0, request)
        self.lock.acquire().addCallback(self._do_get, key)
        return d

    def _do_get(self, lock, key):
        self.transport.write('get %s\r\n' % key)

    def lineReceived(self, line):
        if line == 'STORED':
            req = self.requests.pop()
            d, k, v = req
            reactor.callLater(0, d.callback, k)
            self.lock.release()
        elif line.startswith('VALUE'):
            _, key, __, length = line.split()
            length = int(length)
            self.length = length
            self.buffer = []
            self.value = None
            self.setRawMode()
        elif line == 'END':
            req = self.requests.pop()
            d, k = req
            reactor.callLater(0, d.callback, (k, self.value))
            self.lock.release()
        else:
            print "RECEIVED UNKNOWN LINE", repr(line)


    def rawDataReceived(self, data):
        self.buffer.append(data)
        raw = ''.join(self.buffer)
        if len(raw) >= self.length:
            self.value = raw[:self.length]
            rest = raw[self.length+2:]
            self.setLineMode(rest)






class MemcacheClient(object):
    def __init__(self, host, port=11211):
        self.host = host
        self.port = port
        self.protocol = None
        self.connDefer = defer.Deferred()


    def connect(self):
        if self.protocol is None:

            d.addCallback(got_protocol)
            return d
        else:
            return defer.succeed(None)



    def _cb_set(self, key, value):
        return self.protocol.set(key, value)


    def _cb_get(self, key):
        return self.protocol.get(key)


    def set(self, key, value):
        d = self.connect()
        d.addCallback(lambda _: self._cb_set(key, value))
        return d


    def get(self, key):
        d = self.connect()
        d.addCallback(lambda _: self._cb_get(key))
        return d


if __name__ == '__main__':

    replies = []
    def reply(v):
        replies.append(v)
        return v
    client = protocol.ClientCreator(reactor, MemcacheProtocol)
    def got_protocol(c):
        d1 = c.set('a', '1').addCallback(reply)
        d2 = c.get('a').addCallback(reply)
        d3 = c.set('a', '2').addCallback(reply)
        d4 = c.get('a').addCallback(reply)
        d = defer.gatherResults([d1, d2, d3, d4])
        def finished(res):
            print res
            print replies
            assert replies == ['a',
                ('a', '1'),
                'a',
                ('a', '2'),]
            reactor.stop()
        d.addCallback(finished)
    client.connectTCP('127.0.0.1', 7000).addCallback(got_protocol)



    reactor.run()
