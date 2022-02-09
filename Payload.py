class Payload:

    def __init__(self, client_id="", content=dict()):
        self._client_id = client_id;
        self._content = content;
        self._payload_size = self.calcPayloadSize();

    def calcPayloadSize(self):
        sze = len(self._client_id);
        for key in self._content:
            sze += len(self._content[key]);
        return sze;

    def getPayloadSize(self):
        return self._payload_size;

    def getContent(self):
        return self._content;

    def getClientId(self):
        return self._client_id;
