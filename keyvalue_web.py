from twisted.web.resource import Resource
from twisted.web.server import Site, NOT_DONE_YET
from twisted.web.client import getPage
from twisted.internet import reactor, protocol
from twisted.python import log
import sys

class Index(Resource):
    def render_GET(self, request):
        return """<html><body>
        <form action="/get">
            <h2>Get</h2>
            Key:<input type="text" name="key">
            <input type="submit">
        </form>
        <form action="/set">
            <h2>Set</h2>
            Key:<input type="text" name="key">
            Value:<input type="text" name="value">
            <input type="submit">
        </form>
        <form action="/delete">
            <h2>Delete</h2>
            Key:<input type="text" name="key">
            <input type="submit">
        </form>
        </body></html>"""

class GetPage(Resource):
    def __init__(self, kv):
        Resource.__init__(self)
        self.kv = kv
    def render_GET(self, request):
        key = request.args['key'][0]
        d = self.kv.get(key)
        d.addErrback(lambda f: 'NOT FOUND: %s' % f.getErrorMessage())
        d.addCallback(request.write)
        d.addCallback(lambda _: request.finish())
        return NOT_DONE_YET

class SetPage(Resource):
    def __init__(self, kv):
        Resource.__init__(self)
        self.kv = kv
    def render_GET(self, request):
        key = request.args['key'][0]
        value = request.args['value'][0]
        d = self.kv.set(key, value)
        d.addErrback(lambda f: f.getErrorMessage())
        d.addCallback(request.write)
        d.addCallback(lambda _: request.finish())
        return NOT_DONE_YET

class DeletePage(Resource):
    def __init__(self, kv):
        Resource.__init__(self)
        self.kv = kv
    def render_GET(self, request):
        key = request.args['key'][0]
        d = self.kv.delete(key)
        d.addErrback(lambda f: 'NOT FOUND: %s' % f.getErrorMessage())
        d.addCallback(request.write)
        d.addCallback(lambda _: request.finish())
        return NOT_DONE_YET


def makeSite(kv):
    root = Resource()
    root.putChild('', Index())
    root.putChild('get', GetPage(kv))
    root.putChild('set', SetPage(kv))
    root.putChild('delete', DeletePage(kv))
    factory = Site(root)
    return factory

if __name__ == '__main__':
    from keyvalue_client2 import KeyValueClientProtocol
    log.startLogging(sys.stdout)
    def got_protocol(kv):
        factory = makeSite(kv)
        reactor.listenTCP(8000, factory)

    client = protocol.ClientCreator(reactor, KeyValueClientProtocol)
    d = client.connectTCP('localhost', 11211)
    d.addCallback(got_protocol)
    reactor.run()


