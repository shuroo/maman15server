class Payload:

    def __init__(self,client_id,content=""):
        self._client_id = client_id;
        self._content = content;
        self._payload_size = self.calcPayloadSize();

    def calcPayloadSize(self):
        try:
            sze = len(str(self._client_id));
            sze += len(self._content);
            # for key in self._content:
            #     sze += len(self._content[key]);
        except Exception as e:
            print("Failed to parse size. error:",e);
            sze=0;
        return sze;

    def getPayloadSize(self):
        return self._payload_size;

    def getContent(self):
        return self._content;

    def getClientId(self):
        return self._client_id;
