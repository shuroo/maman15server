
from Response import Response
from Utils import Utils
import struct
# For the fetch clients list operation:
class Response2101(Response):

    def __init__(self, clients_list):
        # todo: add 2101 to constants
        super().__init__(2101, clients_list)
        self.client_list = clients_list ;
        self._payload_size = self.calcRespSize();

        def calcRespSize(self):
            # or 255??
            sze = len(self.clients_list) *(16+256);
            return sze;

        def packResponse(self):
            data = b''
            if (self._payload_size == 0):
                headerStruct = struct(f'< B H I')
                data = headerStruct.pack(self._version, self._response_code, self._payload_size)
                return data;
            headerStruct = struct(f'< B H I  {self._payload_size}s')
            data+= headerStruct.pack(self._version,self._response_code,self._payload_size,self._payload)
            for client in clients_list:
                clientId = client[0]
                userName = bytes(client[1],'ascii')# todo: put in utils #Utils.strFiller(row[1], 256)
                print("usename len:",len(userName))
                print("uid:::", clientId, ",userName::", userName)
                data += struct.pack('<256s', userName)
                data += struct.pack('<16s', clientId)
            return data;