#!/usr/bin/env python

from Constants import Constants
from Utils import Utils

import struct


class Response:

    # todo: EXPEND PARAMS!!
    def __init__(self, response_code, payload):
        self._response_code, self._version, self._payload = response_code, Constants.version, payload
        self._payload_size = self.calcRespSize()

    def calcRespSize(self):
        # self._version.size() = 1
        sze = Constants.size_of_resp_code + Constants.size_of_version + self._payload.getPayloadSize();
        return sze;

    def pack_header(self):
        data = struct.pack('<4sB4s', Utils.strToBytes(str(self._response_code)), self._version,
                           Utils.intToStrFillerWithTrailingZeros(self._payload_size, 4))
        # headerStruct = struct.Struct(f'< 4s B 4s' )  # f< H B I) # < 4s 2s 4s
        # data = headerStruct.pack(Utils.uncodeIntAsString(self._response_code),
        #                          self._version,
        #                          Utils.strFillerWithTrailingZeros(self._payload_size, 4))
        return data;

    def pack_uid(self, uid):
        uid_bytes = uid.bytes;
        return struct.pack('<16s',
                    uid_bytes);

    def pack_pub_key(self, pubKey):
        pk_bytes = Utils.strToBytes(pubKey);
        return struct.pack('<160s',
                    pk_bytes);

    def pack_error(self):
        return struct.pack('<4sB', Utils.strToBytes(self._response_code),
                self._version);


    def pack_response(self):

        if self._response_code == 2100:
            #uid_packed = self._payload.getHeaderParam().bytes;

            data = self.pack_header();
            data += self.pack_uid(self._payload.getHeaderParam())
            return data;
        if self._response_code == 2102:
            print("code = 2102. We shouldn't reach here..!")
            # pl_size = self._payload.getPayloadSize()
            # if pl_size == 0:
            #     return struct.pack('<4sIB', Utils.strToBytes(self._response_code), pl_size, self._version);
            # return struct.pack('<4sBI%ds' % pl_size, Utils.strToBytes(self._response_code), pl_size, self._version,
            #                    self._payload.getContent());

        elif self._response_code == 9000:
            return self.pack_error();
        raise Exception("Unknown response code:",self._response_code)