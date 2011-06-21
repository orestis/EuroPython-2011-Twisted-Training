from twisted.web.resource import Resource
from twisted.web.server import Site, NOT_DONE_YET
from twisted.internet import reactor
from twisted.python import log
import sys
log.startLogging(sys.stdout)

class Index(Resource):

    def render_GET(self, request):
        return "HELLO"


class Page(Resource):
    def render_GET(self, request):
        return 'A PAGE'


class LongRunning(Resource):
    def render_GET(self, request):

        request.write('A')
        reactor.callLater(1, request.write, 'B')
        reactor.callLater(2, request.write, 'C')
        reactor.callLater(3, request.finish)
        return NOT_DONE_YET


root = Resource()
root.putChild('', Index())
root.putChild('page', Page())
root.putChild('long', LongRunning())
factory = Site(root)
reactor.listenTCP(8000, factory)
reactor.run()

