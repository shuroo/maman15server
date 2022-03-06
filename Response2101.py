from UUIDProvider  import UUIDProvider
from Response import Response
from Utils import Utils
from Constants import Constants
import struct
# For the fetch clients list operation:
class Response2101(Response):

    def calcRespSize(self):
        sze = len(self._clients_list) *(Constants.size_of_uid + Constants.size_of_name);
        return sze;

    def __init__(self, clients_list):
        # todo: add 2101 to constants
        self._response_code, self._version, self._payload = Constants.clientsListRespCode, Constants.version, clients_list;
        self._clients_list = clients_list ;
        self._payload_size = self.calcRespSize();

    def pack_clients_list(self):
        data = bytearray();
        for row in self._clients_list:
            clientId = Utils.strToBytes(str(row[0])[:16]) #UUIDProvider.strToUUID(row[0]).bytes;
            userName = Utils.strFillerWithSpaces(row[1], Constants.size_of_name)
            print("uid:::",clientId , ",userName::" , userName )
            data += struct.pack('<%ds' % Constants.size_of_name, Utils.strToBytes(str(userName)))
            data += struct.pack('<%ds' % Constants.size_of_uid, clientId)
        return data;

    # for 2101:
    def pack_response(self):
        data = self.pack_header();
        print("self._payload_size::",self._payload_size)
        if (self._payload_size == 0):
            # data = headerStruct.pack(self._response_code, self._version, self._payload_size)
            return data;
        data += self.pack_clients_list();
        return data;