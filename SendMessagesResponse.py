"""
Class for response to req 140 - return a list of messages for the given user.
"""
from Response import Response
from Message import Message
from Constants import Constants

# For Request 140 - send all messages for the current user:
class SendMessagesResponse(Response):

    def calcRespSize(self):
        """
        Method for calculating the response size.
        :return: the response size.
        """
        lst_messages = self._payload
        sze = Constants.meta_message_size * len(lst_messages);
        for message in lst_messages:
            sze += len(message);
        return sze;

    def __init__(self, lst_messages):
        self._response_code, self._version, self._payload = Constants.msg_received_response_code, Constants.version, lst_messages ;
        self._payload_size = self.calcRespSize();


    # for 2104:
    def pack_response(self):
        """
        Method for packing the response for request 140:
        :return: a buffer of bytearray response with a list of messages.
        """
        data = b''
        data += self.pack_header();
        lst_messages = self._payload;
        for msg_row in lst_messages:
           msg = Message(msg_row)
           data+= msg.pack_message_sent();
        return data;
