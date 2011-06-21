from nose.twistedtools import reactor, deferred
from twisted.internet import protocol, defer
from memset2 import MemsetProtocol

class MockTransport(object):
    def __init__(self):
        self.buffer = []

    def write(self, data):
        self.buffer.append(data)
        
    def value(self):
        return ''.join(self.buffer)

def test_memset_connection():
    p = MemsetProtocol()
    p.transport = mock = MockTransport()
    f = protocol.ClientFactory()
    f.key = 'a'
    f.deferred = defer.Deferred()
    f.value = 'v'
    p.factory = f
    f.timeout = 0.2
    p.connectionMade()
    expectedValue = '\r\n'.join(["set a 0 0 1", 'v', ''])
    assert p.transport.value() == expectedValue
    p.lineReceived('')

@deferred(timeout=1.0)
def test_memset_success():
    p = MemsetProtocol()
    f = protocol.ClientFactory()
    f.key = 'a'
    f.value = 'v'
    f.deferred = d = defer.Deferred()
    p.factory = f
    f.timeout = 0.2

    def stored(key):
        assert key == 'a'
    d.addCallback(stored)

    p.lineReceived('STORED')
    return d

@deferred(timeout=1.0)
def test_memset_failure():
    p = MemsetProtocol()
    f = protocol.ClientFactory()
    f.key = 'a'
    f.value = 'v'
    f.deferred = d = defer.Deferred()
    p.factory = f
    f.timeout = 0.2

    def failed(f):
        assert f.getErrorMessage() == "bad bad bad"
    d.addErrback(failed)

    p.lineReceived('CLIENT_ERROR bad bad bad')
    return d

@deferred(timeout=2.0)
def test_memset_timeout():
    p = MemsetProtocol()
    p.transport = mock = MockTransport()
    f = protocol.ClientFactory()
    f.key = 'a'
    f.value = 'v'
    f.timeout = 0.2
    f.deferred = d = defer.Deferred()
    p.factory = f

    p.connectionMade()

    def failed(f):
        assert f.getErrorMessage() == "Timeout"
    d.addErrback(failed)

    return d


