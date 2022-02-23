#!/usr/bin/env python

from Constants import Constants
from Utils import Utils

import struct


class Response:

    # todo: EXPEND PARAMS!!
    def __init__(self, response_code, payload): # client_id="", , clientName="", messageId=""
        self._response_code, self._version, self._payload = response_code, Constants.version, payload;
        self._payload_size = self.calcRespSize();

    def calcRespSize(self):
        # self._version.size() = 1
        sze = len(self._response_code) + len(str(self._version))  + self._payload.getPayloadSize();
        return sze;

    def pack_response(self):
        if self._response_code == '2100':
            uid_packed = self._payload.getClientId().bytes;
            print('clientId before Packing:', self._payload.getClientId())
            return struct.pack('<4sB16s', Utils.strToBytes(self._response_code),self._version,
                             uid_packed);
        if self._response_code == '2102':
            pl_size = self._payload.getPayloadSize()
            if( pl_size == 0 ):
                return struct.pack('<4sIB', Utils.strToBytes(self._response_code), pl_size, self._version);
            return struct.pack('<4sBI%ds'% pl_size, Utils.strToBytes(self._response_code),pl_size, self._version,
                             self._payload.getContent());
        elif self._response_code == '2101':
            pl_size = self._payload.getPayloadSize()
            if( pl_size == 0 ):
                return struct.pack('<4sIB', Utils.strToBytes(self._response_code), pl_size, self._version);
            clients_list =self._payload.getContent()
            data = b''
            for row in clients_list:
                clientId , userName, publicKey = row[0] ,row[1], row[2]
                print(clientId , "," , userName , "," , publicKey)
                data += struct.pack('<16s', clientId)
                data += struct.pack('<256s', Utils.strToBytes(str(userName)))
                data += struct.pack('<161s', publicKey) # "userName"
            data = struct.pack('<4sIB', Utils.strToBytes(self._response_code), pl_size, self._version) + data;
            return data;

        elif self._response_code == '9000':
            return struct.pack('<4sB', Utils.strToBytes(self._response_code) ,
                    self._version);
        raise Exception("Unknown response code:",self._response_code)
