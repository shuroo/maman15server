
from Response import Response
from Utils import Utils
from Constants import Constants
import struct
# For the fetch clients list operation:
class Response2101(Response):


    def calcRespSize(self):
        sze = len(self._clients_list) *(Constants.sizeOfUid+Constants.sizeOfName);
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
            userName = Utils.strFillerWithSpaces(row[1], Constants.sizeOfName)
            print("uid:::",clientId , ",userName::" , userName )
            data += struct.pack('<%ds' % Constants.sizeOfName, Utils.strToBytes(str(userName)))
            data += struct.pack('<%ds' % Constants.sizeOfUid, clientId)
        return data;

    # for 2101:
    def pack_response(self):
        data = b''
        headerStruct =  struct.Struct(f'< 4s 1s 4s')

            #struct.Struct(f'< 4s 1s 4s')
        #             headerStruct = struct.Struct(f'< H B I')
        #             data = headerStruct.pack(self._response_code, self._version, self._payload_size)
        #             return data;
        data = headerStruct.pack(Utils.uncodeIntAsString(self._response_code),
                                 Utils.strFillerWithTrailingZeros(self._version,2), # Utils.uncodeIntAsString(
                                 Utils.strFillerWithTrailingZeros(self._payload_size,4))

        print("self._payload_size::",self._payload_size)
        if (self._payload_size == 0):
            # data = headerStruct.pack(self._response_code, self._version, self._payload_size)
            return data;
        data += self.pack_clients_list();
        return data;