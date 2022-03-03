class Payload:

    def __init__(self, header_param, content=""):
        self._header_param = header_param;
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

    # General header param: name , message or client id.
    def getHeaderParam(self):
        return self._header_param;
