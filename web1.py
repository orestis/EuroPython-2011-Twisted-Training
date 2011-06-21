from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.internet import reactor
from twisted.python import log
import sys
log.startLogging(sys.stdout)


root = Resource()
factory = Site(root)
reactor.listenTCP(8000, factory)
reactor.run()
