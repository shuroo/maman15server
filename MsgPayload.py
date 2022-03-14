from UUIDProvider import UUIDProvider

from Payload import Payload;
from Utils import Utils;


class MsgPayload(Payload):
    counter = 0

    def __init__(self, client_id,msg_type, content_sz=0, msg_content=""): # header_param, content
        super().__init__(client_id,msg_content);
        self._msg_type = msg_type;
        self._content_sz = content_sz;
        self._payload_size = self.calcPayloadSize();
        MsgPayload.counter += 1
        print('MsgPayload.counter = ',MsgPayload.counter)
        self.counter = MsgPayload.counter;
        self._msg_id = self.counter #Utils.strFillerWithTrailingZeros(str(self.counter),4);

    def getMessageType(self):
        return self._msg_type;

    def getContentSz(self):
        return self._content_sz;

    def getMsgId(self):
        return self._msg_id;
