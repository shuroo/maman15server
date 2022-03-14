import struct
from Utils import Utils
class PackUtils:

    @staticmethod
    def pack_single_int(int_to_pack):
        return struct.pack('<I',
                    int_to_pack);

    @staticmethod
    def pack_string(str_to_pack,sz=-1):
        if sz == -1:
            sz = len(str_to_pack)
        return struct.pack('<%ds' % sz, Utils.strToBytes(str_to_pack));