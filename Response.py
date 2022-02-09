#!/usr/bin/env python

from Constants import Constants
from Utils import Utils

import struct
from Payload import Payload;


# def clientIdTo16Filler(self):
#     return Utils.strFiller(self._client_id,16);


class Response:

    # todo: EXPEND PARAMS!!
    def __init__(self, response_code, payload=Payload()): # client_id="", , clientName="", messageId=""
        self._response_code, self._version, self._payload = response_code, Constants.version, payload;
        self._payload_size = self.calcRespSize();

    def calcRespSize(self):
        # self._version.size() = 1
        sze = len(self._response_code) + len(str(self._version))  + self._payload.getPayloadSize();
        return sze;

    def pack_response(self):
        if self._response_code == '2100':
            return struct.pack('<4s16sB', Utils.strToBytes(self._response_code),
                             Utils.strToBytes(self._payload.getClientId()),
                    self._version);
        elif self._response_code == '9000':
            return struct.pack('<4sB', Utils.strToBytes(self._response_code) ,
                    self._version);
        raise Exception("Unknown response code:",self._response_code)
