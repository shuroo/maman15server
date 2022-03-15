#!/usr/bin/env python
"""
Class for constructing general server responses.
"""
from Constants import Constants
from Utils import Utils

import struct


class Response:

    def __init__(self, response_code, payload):
        self._response_code, self._version, self._payload = response_code, Constants.version, payload
        self._payload_size = self.calcRespSize()

    def calcRespSize(self):
        """Method for calculating the response size."""
        sze = Constants.size_of_resp_code + Constants.size_of_version + self._payload.getPayloadSize();
        return sze;

    def pack_header(self):

        """Method for building the response header: version, pl_size, response-code."""
        data = struct.pack('<4sB4s', Utils.strToBytes(str(self._response_code)), self._version,
                           Utils.intToStrFillerWithTrailingZeros(self._payload_size, 4))
        return data;

    def pack_uid(self, uid):

        """Method for packing the client id (unique id, uuid) as a string."""
        uid_bytes = uid.bytes;
        return struct.pack('<16s',
                    uid_bytes);

    def pack_pub_key(self, pubKey):
        """Method for public key pack to send to client buffer."""
        pk_bytes = Utils.strToBytes(pubKey);
        return struct.pack('<160s',
                    pk_bytes);

    def pack_error(self):
        return struct.pack('<4sB', Utils.strToBytes(self._response_code),
                self._version);


    def pack_response(self):

        if self._response_code == 2100:
            data = self.pack_header();
            data += self.pack_uid(self._payload.getHeaderParam())
            return data;
        elif self._response_code == 9000:
            return self.pack_error();
        raise Exception("Unknown response code:",self._response_code)