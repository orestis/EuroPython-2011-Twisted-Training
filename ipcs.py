from twisted.spread import pb
from twisted.internet import reactor

class RDict(pb.Root):
    def remote_get(self, key):
        return key

reactor.listenTCP(8789,
    pb.PBServerFactory(RDict()))
reactor.run()
