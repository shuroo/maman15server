#!/usr/bin/env python

from Constants import Constants
from Utils import Utils

import struct


class Response:

    # todo: EXPEND PARAMS!!
    def __init__(self, response_code, payload):
        self._response_code, self._version, self._payload = response_code, Constants.version, payload;
        self._payload_size = self.calcRespSize();

    def calcRespSize(self):
        # self._version.size() = 1
        sze = Constants.size_of_resp_code + Constants.size_of_version + self._payload.getPayloadSize();
        return sze;

    def pack_header(self):
        headerStruct = struct.Struct(f'< 4s B 4s' )  # f< H B I) # < 4s 2s 4s
        data = headerStruct.pack(Utils.uncodeIntAsString(self._response_code),
                                 self._version,
                                 Utils.strFillerWithTrailingZeros(self._payload_size, 4))
        return data;

    def packUid(self,uid):
        uid_bytes = uid.bytes;
        return struct.pack('<16s',
                    uid_bytes);

    def packPubKey(self,pubKey):
        pk_bytes = Utils.strToBytes(pubKey);
        return struct.pack('<160s',
                    pk_bytes);

    def pack_response(self):
        if self._response_code == 2100:
            data = self.pack_header();
            uid_packed = self._payload.getHeaderParam();
            data += self.packUid(uid_packed);
            return data;

        # todo: add error. should not reach here but to the sub class
        # elif self._response_code == '2101':
        #     pl_size = self._payload.getPayloadSize()
        #     if( pl_size == 0 ):
        #         return struct.pack('<4sIB', Utils.strToBytes(self._response_code), pl_size, self._version);
        #     clients_list =self._payload.getContent()
        #     data = b''
        #
        #     data += struct.pack(f'< B H I  ', Utils.strToBytes(str(userName)))
        #     for row in clients_list:
        #         clientId = row[0]
        #         userName = Utils.strFiller(row[1],256)
        #         print("uid:::",clientId , ",userName::" , userName )
        #         data += struct.pack('<256s', Utils.strToBytes(str(userName)))
        #         data += struct.pack('<16s', clientId)
        #     data = struct.pack('<4sIB', Utils.strToBytes(self._response_code), pl_size, self._version) + data;
        #     return data;

        elif self._response_code == '9000':
            return struct.pack('<4sB', Utils.strToBytes(self._response_code) ,
                    self._version);
        raise Exception("Unknown response code:",self._response_code)
