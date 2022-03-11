from Payload import Payload;

class MsgPayload(Payload):
    def __init__(self, client_id,msg_type, content_sz=0, msg_content=""): # header_param, content
        super.__init__(client_id,msg_content);
        _msg_type = msg_type;
        _content_sz = content_sz;
        self._payload_size = self.calcPayloadSize();

        def getMsgType(self):
            return self._msg_type;

        def getContentSz(self):
            return self._content_sz;
