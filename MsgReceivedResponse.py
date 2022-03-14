#For adding messages response,  resp_code = 1103:

from Response import Response
from Constants import Constants
from PackUtils import PackUtils

class MsgReceivedResponse(Response):

    def calcRespSize(self):
        sze = 2* Constants.size_of_uid;
        return sze;

    def __init__(self, msgId,clientId):
        self._response_code, self._version, self._payload = Constants.msg_received_response_code, Constants.version, \
                                                            (msgId, clientId);
        self._payload_size = self.calcRespSize();

    def pack_message_received(self):
        data = b''
        data += self.pack_header();
        if self._payload_size == 0:
            return data;
        dst_client_id = self._payload[0]
        msg_id = self._payload[1];
        data += PackUtils.pack_single_int(msg_id)
        data += PackUtils.pack_string(dst_client_id)
        return data;

    # for 2103:
    def pack_response(self):
        data = self.pack_message_received();
        return data;
