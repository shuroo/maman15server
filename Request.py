#!/usr/bin/env python
class Request:

    def __init__(self,client_name,version , req_code , payload_size , message_type, payloadObj):
        self._client_name = client_name;
        self._version = version;
        self._req_code = req_code;
        self._payload_size = payload_size;
        self._message_type = message_type;
        self._payload = payloadObj;

    def getClientName(self):
        return self._client_name;

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

#
# if __name__ == "__main__":
#     print("Python {0:s} {1:d}bit on {2:s}\n".format(" ".join(elem.strip() for elem in sys.version.split("\n")), 64 if sys.maxsize > 0x100000000 else 32, sys.platform))
#     main(*sys.argv[1:])
#     print("\nDone.")