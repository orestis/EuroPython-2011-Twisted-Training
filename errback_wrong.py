from twisted.internet import reactor, defer



def on_success(msg):
    print 'SUCCESS', msg

def on_error(f):
    print 'ERROR', f.getErrorMessage()


d1 = defer.Deferred()
d1.addCallback(on_success)
d1.addErrback(on_error)
reactor.callLater(1, d1.callback, 'NEAT')
reactor.callLater(2, d1.errback, Exception('BUMMER'))


reactor.run()
