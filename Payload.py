class Payload:

    def __init__(self, psize, content, public_key):
        self._payload_size = psize;
        self._content = content;
        self._public_key = public_key;

    def getPayloadSize(self):
        return self._payload_size;

    def getContent(self):
        return self._content;

    def getPublicKey(self):
        return self._public_key;
