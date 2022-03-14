#For adding messages response,  resp_code = 1103:

from UUIDProvider import UUIDProvider

from Response import Response
from Message import Message
from Constants import Constants

# For Request 140 - send all messages for the current user:
class SendMessagesResponse(Response):

    def calcRespSize(self):
        sze = Constants.meta_message_size * len(self.lst_messages);
        for message in self.lst_messages:
            sze += len(message.content);
        return sze;

    def __init__(self, lst_messages):
        self._response_code, self._version, self._payload = Constants.msg_received_response_code, Constants.version, lst_messages ;
        self._payload_size = self.calcRespSize();


    # for 2104:
    def pack_response(self):
        data = b''
        data += self.pack_header();
        lst_messages = self._payload;
        for msg_row in lst_messages:
           msg = Message(msg_row)
           data+= msg.pack_message_sent();
        return data;
