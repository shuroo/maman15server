
from Response import Response
from Utils import Utils
from Constants import Constants
import struct
# For the fetch clients list operation:
class Response2102(Response):

    def calcRespSize(self):
        sze = Constants.size_of_uid + Constants.size_of_public_key;
        return sze;

    def __init__(self, pubKey,clientId):
        self._response_code, self._version, self._payload = Constants.pubKRespCode, Constants.version, (pubKey,clientId);
        self._payload_size = self.calcRespSize();

    # for 2102:
    def pack_response(self):
        data = b''
        data += self.pack_header();
        if (self._payload_size == 0):
            # data = headerStruct.pack(self._response_code, self._version, self._payload_size)
            return data;
        data += self.packPubKey(self._payload[0]);
        data += self.packUid(self._payload[1]);
        return data;
