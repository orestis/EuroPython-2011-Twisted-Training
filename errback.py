from twisted.internet import reactor, defer


def on_success(msg):
    print 'SUCCESS', msg

def on_error(f):
    print 'ERROR', f.getErrorMessage()


d1 = defer.Deferred()
d1.addCallback(on_success)
d1.addErrback(on_error)
reactor.callLater(1, d1.callback, 'NEAT')

d2 = defer.Deferred()
d2.addCallback(on_success)
d2.addErrback(on_error)
reactor.callLater(2, d2.errback, Exception('BUMMER'))


reactor.run()
