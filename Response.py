#!/usr/bin/env python

from Request import Request


class Response(Request):

    def __init__(self,client_name,message_id, client_id,version , req_code ,
                 payload_size , message_type, payload_content):
        super().__init__(self,client_id,version , req_code , payload_size ,
                         message_type, payload_content)
        self._client_name = client_name;
        self._message_id = message_id;
