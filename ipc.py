from twisted.spread import pb
from twisted.internet import reactor

factory = pb.PBClientFactory()
reactor.connectTCP("localhost", 8789,
    factory)
d = factory.getRootObject()
def got_root(root):
    d = root.callRemote("get", "key")
    def got_value(v):
        print v
        reactor.stop()
    d.addCallback(got_value)
d.addCallback(got_root)
reactor.run()
