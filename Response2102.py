from UUIDProvider import UUIDProvider

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
        self._response_code, self._version, self._payload = Constants.pub_k_resp_code, Constants.version, (pubKey, clientId);
        self._payload_size = self.calcRespSize();

    # for 2102:
    def pack_response(self):
        data = b''
        data += self.pack_header();
        if (self._payload_size == 0):
            # data = headerStruct.pack(self._response_code, self._version, self._payload_size)
            return data;
        data += self.pack_pub_key(self._payload[0]);
        print('pub key in resp 2102:', self._payload[0])
        uid_obj = UUIDProvider.strToUUID(self._payload[1][0][1]);
        data += self.pack_uid(uid_obj);
        return data;
