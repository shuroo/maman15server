# Message class \ struct
from Utils import Utils
from PackUtils import PackUtils

class Message:

    def __init__(self,msg_row):
        self.msg_id = msg_row[0]
        self.to_client = msg_row[1]
        self.from_client = msg_row[2]
        self.msg_type = msg_row[3]
        self.content = msg_row[4]

    def pack_message_sent(self):
        data = b''
        data += self.pack_header();
        if self._payload_size == 0:
            return data;
        data += PackUtils.pack_single_int(self.msg_id)
        data += PackUtils.pack_string(self.from_client)
        data += PackUtils.pack_char(self.msg_type)
        data += PackUtils.pack_single_int(self.msg_size)
        data += PackUtils.pack_string(self.content)

        return data;