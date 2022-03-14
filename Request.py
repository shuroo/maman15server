#!/usr/bin/env python
class Request:

    def __init__(self,client_name_or_id,version , req_code , payload_size , payloadObj):
        self._client_name_id = client_name_or_id;
        self._version = version;
        self._req_code = req_code;
        self._payload_size = payload_size;
        self._payload = payloadObj;

    def getClientNameOrId(self):
        return self._client_name_id;

    def getVersion(self):
        return self._version;

    def getRequestCode(self):
        return self._req_code;

    def getPayloadSize(self):
        return self._payload_size;

    def getMessageType(self):
        return self._message_type;

    def getPayloadObject(self):
        return self._payload;