#For adding messages response,  resp_code = 1103:

from UUIDProvider import UUIDProvider

from Response import Response
from Utils import Utils
from Constants import Constants
import struct
# For the fetch clients list operation:
class MsgResponse(Response):

    def calcRespSize(self):
        sze = 2* Constants.size_of_uid;
        return sze;

    def __init__(self, msgId,clientId):
        self._response_code, self._version, self._payload = Constants.msgResponseCode, Constants.version, (msgId,clientId);
        self._payload_size = self.calcRespSize();

    def pack_msg_id(self, msg_id):
        # todo: also possible to pack as an int : struct.pack('<I',                     msg_id)
        #msg_id_bytes = Utils.uncodeIntAsString(msg_id);
        return struct.pack('<I',
                    msg_id);

    # for 2103:
    def pack_response(self):
        data = b''
        data += self.pack_header();
        if self._payload_size == 0:
            # data = headerStruct.pack(self._response_code, self._version, self._payload_size)
            return data;

        dst_client_id = self._payload[0]
        msg_id = self._payload[1];
        data += self.pack_msg_id(msg_id);
        print('msg id  in resp 2103:', msg_id)
        data += Utils.strToBytes(dst_client_id);
        return data;
