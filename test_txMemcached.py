from nose.twistedtools import reactor, deferred
from twisted.internet import defer

import unittest

from txMemcached import MemcacheProtocol
from mock import Mock

class MockTransport(object):
    def __init__(self):
        self.buffer = []

    def write(self, d):
        self.buffer.append(d)

    def value(self):
        return ''.join(self.buffer)


class TextInterleavedProtocol(unittest.TestCase):
    def setUp(self):
        self.protocol = MemcacheProtocol()
        self.protocol.transport = Mock()


    @deferred(timeout=1.0)
    def test_connection(self):
        d = self.protocol.connectedDeferred
        self.protocol.connectionMade()
        return d


    @deferred(timeout=1.0)
    def test_set_simple(self):
        m = self.protocol.transport
        d = self.protocol.set("a", "value")
        self.protocol.lineReceived('STORED')
        def wrote(key):
            assert key == "a"
        d.addCallback(wrote)
        return d



    @deferred(timeout=1.0)
    def test_get_simple(self):
        m = self.protocol.transport
        d = self.protocol.get("a")
        self.protocol.lineReceived('VALUE a 0 5')
        self.protocol.rawDataReceived("abcde\r\n")
        self.protocol.lineReceived('END')
        def got((key, value)):
            assert key == "a"
            assert value == "abcde"
        d.addCallback(got)
        return d


    @deferred(timeout=1.0)
    def DONTtest_set_multiple(self):
        m = self.protocol.transport = MockTransport()
        d1 = self.protocol.set("a", "1")
        reactor.callLater(0, self.protocol.lineReceived, "STORED")
        assert self.protocol.lock.locked
        def wrote_1(key):
            assert key == "a"
            assert m.value() == '\r\n'.join(["set a 0 0 1", "1", ""])
            m.buffer = []
            assert self.protocol.lock.locked
            reactor.callLater(0, self.protocol.lineReceived, "STORED")
        d1.addCallback(wrote_1)
        d2 = self.protocol.set("b", "2")
        final_d = defer.Deferred()
        def wrote_2(key):
            assert key == "b"
            assert m.value() == '\r\n'.join(["set b 0 0 1", "2", ""])
            assert self.protocol.lock.locked
            reactor.callLater(0, final_d.callback, None)
        d2.addCallback(wrote_2)
        def final(_):
            assert not self.protocol.lock.locked
        final_d.addCallback(final)
        return final_d


    @deferred(timeout=1.0)
    def DONTtest_get_multiple(self):
        m = self.protocol.transport = MockTransport()
        d1 = self.protocol.get("a")
        assert self.protocol.lock.locked
        def send(k, v):
            self.protocol.lineReceived('VALUE %s 0 %d' % (k, len(v)))
            self.protocol.rawDataReceived("%s\r\n" % v)
            self.protocol.lineReceived('END')
        reactor.callLater(0, send, "a", "123")
        def got_a((k, v)):
            assert k == 'a'
            assert v == '123'
            assert self.protocol.lock.locked
            assert m.value() == 'get a\r\n'
            assert [k for (_, k) in self.protocol.requests] == ['b']
            m.buffer = []
            reactor.callLater(0, send, "b", "456")
        d1.addCallback(got_a)
        d2 = self.protocol.get("b")
        final_d = defer.Deferred()
        def got_b((k, v)):
            assert k == 'b'
            assert v == '456'
            assert self.protocol.lock.locked
            assert m.value() == 'get b\r\n'
            m.buffer = []
            assert [k for (_, k) in self.protocol.requests] == []
            reactor.callLater(0, final_d.callback, None)
        d2.addCallback(got_b)
        def final(_):
            assert not self.protocol.lock.locked
        final_d.addCallback(final)
        assert [k for (_, k) in self.protocol.requests] == ['b', 'a']
        return final_d


