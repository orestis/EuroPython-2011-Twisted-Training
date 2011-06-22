from keyvalue_web import makeSite
from twisted.internet import reactor
from twisted.spread import pb

if __name__ == '__main__':
    factory = pb.PBClientFactory()
    reactor.connectTCP(8789, factory)



