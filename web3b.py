from twisted.web.resource import Resource
from twisted.web.server import Site, NOT_DONE_YET
from twisted.web.client import getPage
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
        url = request.args['url'][0]
        d = getPage(url)
        d.addCallback(request.write)
        d.addCallback(lambda _: request.finish())
        return NOT_DONE_YET


root = Resource()
root.putChild('', Index())
root.putChild('page', Page())
root.putChild('long', LongRunning())
factory = Site(root)
reactor.listenTCP(8000, factory)
reactor.run()

