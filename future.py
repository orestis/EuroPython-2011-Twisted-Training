from twisted.internet import reactor

def print_it(p):
    print p

reactor.callLater(5, print_it, 'HI')
reactor.callLater(6, reactor.stop)

reactor.run()
