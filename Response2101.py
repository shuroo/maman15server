
from Response import Response
from Utils import Utils
from Constants import Constants
import struct
# For the fetch clients list operation:
class Response2101(Response):


    def calcRespSize(self):
        sze = len(self._clients_list) *(16+256);
        return sze;

    def __init__(self, clients_list):
        # todo: add 2101 to constants
        self._response_code, self._version, self._payload = '2101', Constants.version, clients_list;
        self._clients_list = clients_list ;
        self._payload_size = self.calcRespSize();

    def pack_clients_list(self):
        data = bytearray();
        for row in self._clients_list:
            clientId = row[0]
            userName = Utils.strFiller(row[1],256)
            print("uid:::",clientId , ",userName::" , userName )
            data += struct.pack('<256s', Utils.strToBytes(str(userName)))
            data += struct.pack('<16s', clientId)

    # for 2101:
    def pack_response(self):
        print("Inside Child1")
        data = b''
        headerStruct = struct.Struct(f'< 4s 1s 4s')
        #             headerStruct = struct.Struct(f'< H B I')
        #             data = headerStruct.pack(self._response_code, self._version, self._payload_size)
        #             return data;
        data = headerStruct.pack(Utils.uncodeIntAsString(self._response_code), Utils.uncodeIntAsString(self._version),
                                 Utils.uncodeIntAsString(self._payload_size))
        if (self._payload_size == 0):
            # data = headerStruct.pack(self._response_code, self._version, self._payload_size)
            return data;
        for client in self._clients_list:
            clientId =  client[0];
            userName = bytes(Utils.strFiller(client[1],256),'ascii')# todo: put in utils #Utils.strFiller(row[1], 256)
            print("usename len:",len(userName))
            print("uid:::", clientId, ",userName::", userName)
            data += struct.pack('<256s', userName)
            data += struct.pack('<16s', clientId)
        return data;