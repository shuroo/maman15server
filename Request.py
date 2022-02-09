#!/usr/bin/env python
class Request:

    def __init__(self,client_id,version , req_code , payload_size , message_type, payload_content):
        self._client_id = client_id;
        self._version = version;
        self._req_code = req_code;
        self._payload_size = payload_size;
        self._message_type = message_type;
        self._payload_content = payload_content;

    def getClientName(self):
        return self._client_id;

    def getVersion(self):
        return self._version;

    def getRequestCode(self):
        return self._req_code;

    def getPayloadSize(self):
        return self._payload_size;

    def getMessageType(self):
        return self._message_type;

    def getPayloadContent(self):
        return self._payload_content;

import sys
import ctypes
import struct
#
# class Request(ctypes.Structure):
#
#     _fields_ = [
#         ("client_id", ctypes.c_char),
#         ("code", ctypes.c_int),
#         ("version", ctypes.c_int)
#
#
#         # 	char* clientId = new char[256];
#         # 	// todo: set payload size here in the future.
#         # 	unsigned int payload_size;
#         # 	unsigned int version;
#         # 	unsigned int code;
#     ]
#
#
# def main(*argv):
#     #data = b'\x02\x00\x00\x00'
#     text = bytes("abbba 3 110\x00",'UTF-8')
#
#     txtWithLen = struct.pack('B%ds' % len(text), len(text), text)
#     length = struct.unpack("B", txtWithLen[0:1])[0]
#     # clientId = struct.unpack("%ds" % 6, txtWithLen[1:6])[0]
#     # version = struct.unpack("B", txtWithLen[7:8])[0]
#     # code = struct.unpack("b", txtWithLen[9:])[0]
#     gvrTxt = struct.unpack("%ds" % length, txtWithLen[1:])[0]
#     indexOfNull = gvrTxt.index(b'\x00')
#     print(gvrTxt[:indexOfNull])
#
#
#
#     fmt = ">s"
#     #clientid = struct.unpack(fmt, data[:4])[0]
#     #print(clientid)#"Fields\n  clientId: {:d}\n  ".format(data.decode()))
#     #data = struct.pack("s", socket.htonl("abbba"))
#     # #print(data)
#     # #print(socket.ntohl(struct.unpack("s", data)[0]))
#   #  x = Request()
#   #  fmt = ">cii"
#     # clientid = struct.unpack(fmt, data[:4])[0]
#     # code = struct.unpack(fmt, data[4:5])[0]
#     # version = struct.unpack(fmt, data[5:6])[0]
#
#  #   fmt_size = struct.calcsize(fmt)
# #    x.clientId , x.code ,  x.version = struct.unpack(fmt, data[:fmt_size])
# #    print("Fields\n  clientId: {:d}\n  ".format(data.decode()))
#
#
#
# if __name__ == "__main__":
#     print("Python {0:s} {1:d}bit on {2:s}\n".format(" ".join(elem.strip() for elem in sys.version.split("\n")), 64 if sys.maxsize > 0x100000000 else 32, sys.platform))
#     main(*sys.argv[1:])
#     print("\nDone.")