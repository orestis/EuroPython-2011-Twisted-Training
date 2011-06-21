from twisted.web.resource import Resource
from twisted.web.server import Site, NOT_DONE_YET
from twisted.internet import reactor, defer, threads
from twisted.python import log
import sys
log.startLogging(sys.stdout)

def fib(target):
    first = 0
    second = 1

    for i in xrange(target - 1):
        new = first + second
        first = second
        second = new
    return second


class Fibonacci(Resource):
    def render_GET(self, request):
        num = int(request.args['num'][0])

        request.write('Result is: ')
        d = defer.Deferred()
        d = threads.deferToThread(fib, num)
        d.addCallback(lambda n: request.write('%s digits long\r\n' % len(str(n))))
        d.addCallback(lambda _: request.finish())

        return NOT_DONE_YET


root = Resource()
root.putChild('', Fibonacci())
factory = Site(root)
reactor.listenTCP(8000, factory)
reactor.run()

