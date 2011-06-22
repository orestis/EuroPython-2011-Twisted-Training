from twisted.internet import reactor

class KeyValueStore(object):
    def __init__(self):
        self.store = {}
        self.timeouts = {}

    def get(self, key):
        return self.store[key]

    def set(self, key, value):
        self._cancelTimeout(key)
        self.store[key] = value
        self.timeouts[key] = reactor.callLater(15, self.delete, key)
        return key

    def delete(self, key):
        self._cancelTimeout(key)
        del self.store[key]

    def _cancelTimeout(self, key):
        delayedCall = self.timeouts.pop(key, None)
        if delayedCall and delayedCall.active():
            delayedCall.cancel()
