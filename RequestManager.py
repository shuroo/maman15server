from UUIDProvider import UUIDProvider
from SQLOperations import SQLOperations
from Response import Response
from Response2101 import Response2101
from SimplePayload import SimplePayload
from Payload import Payload
from Response2102 import Response2102
from MsgResponse import MsgResponse

class RequestManager:

    def handle_general_errors(self):
        msg = "9000 Error Raised and Sent!!"
        print(msg)
        response = Response(9000, SimplePayload(msg))
        reply = response.pack_response()
        return reply;

    # For Request 120:
    def handle_create_client_request(self,conn, request):
        ident = UUIDProvider.createUniqueID()
        SQLOperations.add_client(request.getClientNameOrId(), ident, conn, request)
        response = Response(2100, Payload(ident))
        reply = response.pack_response()
        return reply;

    # For Request 120:
    def handle_clients_list_request(self,conn, request):
        clients_list = SQLOperations.get_clients_list(conn);
        print('clients list resp 120 first item::::',clients_list[0][0],",,",clients_list[0][1])
        response = Response2101(clients_list)
        reply = response.pack_response()
        return reply;

    # For Request 130:

    def handle_public_key_request(self,conn, req):
        client_id = req.getPayloadObject().getHeaderParam()
        pub_key = SQLOperations.select_public_key(conn,client_id);
        response = Response2102(client_id,pub_key)
        reply = response.pack_response()
        return reply;

    # For Request 140:
    def handle_get_client_messages_request(self,conn, request):
        print("reached handle_get_client_messages_request!!!!")
        messages = SQLOperations.select_client_messages(conn,request);
        return messages;

    # # For Request 150:
    def handle_create_message_request(self,conn,request):
        print("reached handle_create_message_request!!!! payload:",request.getPayloadObject())
        (client_id,msg_id) = SQLOperations.create_client_message(conn,request);
        response = MsgResponse(client_id,msg_id)
        reply = response.pack_response()
        return reply;

    # TBD: Requests: 150,151,152,153,0

    def handle_request(self, conn, *args):
        try:
            request = args[0];
            request_code = request.getRequestCode();
            # 110 - register: - reply should be 2100 when ok or 9000 - otherwise
            if request_code == 1100:
                pubKey = self.handle_create_client_request(conn,request);
                return pubKey;
            # 120 - clients list: - reply should be __ when ok or 9000 - otherwise
            if request_code == 1101:
                clients_list = self.handle_clients_list_request(conn,request);
                return clients_list;
            # 130 - clients list: - reply should be __ when ok or 9000 - otherwise
            if request_code == 1102:
                pubKey = self.handle_public_key_request(conn,request);
                return pubKey;
            # 140 - clients list: - reply should be __ when ok or 9000 - otherwise
            if request_code == 1104:
                cl_msgs = self.handle_get_client_messages_request(conn,request);
                return cl_msgs;
            # 150 - clients list: - reply should be __ when ok or 9000 - otherwise
            if request_code == 1103:
                client_msg_id = self.handle_create_message_request(conn,request);
                return client_msg_id;
        except Exception as err:
            print('Failed to handle request. Error raised:', err);
            return self.handle_general_errors()
        return 0
