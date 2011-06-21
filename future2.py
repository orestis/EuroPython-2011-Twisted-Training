from twisted.internet import reactor

def print_it(p):
    print p

delayedCall = reactor.callLater(5, print_it, 'HI')
def abort():
    if delayedCall.active():
        print 'CANCELLING'
        delayedCall.cancel()
reactor.callLater(4, abort)
reactor.callLater(6, reactor.stop)

reactor.run()
