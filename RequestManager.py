"""

Class for managing the different client requests , 110 - 152:

"""


from UUIDProvider import UUIDProvider
from SQLOperations import SQLOperations
from Response import Response
from Response2101 import Response2101
from SimplePayload import SimplePayload
from Payload import Payload
from Response2102 import Response2102
from MsgReceivedResponse import MsgReceivedResponse
from SendMessagesResponse import SendMessagesResponse

class RequestManager:


    def handle_general_errors(self,err):
        """
        General Method for Error handling. returns status 9000.
        """
        msg = ("Failed to parse request. an error occured. Error:",err)
        print(msg)
        response = Response(9000, SimplePayload(msg))
        reply = response.pack_response()
        return reply;

    # For Request 110:
    def handle_create_client_request(self,conn, request):
        """
        Register User - Method for request 110 to create a new client.
        """
        ident = UUIDProvider.createUniqueID()
        response=''
        try:
            SQLOperations.add_client(request.getClientNameOrId(), ident, conn, request)
            response = Response(2100, Payload(ident))
        except:
            msg = "Failed To Add client. Please Note that the name should be unique!"
            print(msg)
            response = Response(9000, Payload(msg))
        reply = response.pack_response()
        return reply;


    # For Request 120:
    def handle_clients_list_request(self,conn, request):
        """
        Get Clients list - Method for request 120 to get the clients list.
        """
        clients_list = SQLOperations.get_clients_list(conn)
        response = Response2101(clients_list)
        reply = response.pack_response()
        return reply;

    # For Request 130:

    def handle_public_key_request(self,conn, req):
        """
        Generate public key - Method for request 130 to save a public key.
        """
        client_id = req.getPayloadObject().getHeaderParam()
        pub_key = SQLOperations.select_public_key(conn,client_id);
        response = Response2102(client_id,pub_key)
        reply = response.pack_response()
        return reply;

    # For Request 140:
    def handle_get_client_messages_request(self,conn, request):
        """
        Get Client Messages - Method for request 140 to fetch user messages.
        """
        messages = SQLOperations.select_client_messages(conn,request);
        response = SendMessagesResponse(messages)
        reply = response.pack_response()
        return reply;

    # # For Request 150:
    def handle_create_message_request(self,conn,request):
        (client_id,msg_id) = SQLOperations.create_client_message(conn,request);
        response = MsgReceivedResponse(client_id, msg_id)
        reply = response.pack_response()
        return reply;

    # TBD: Requests: 150,151,152,153,0

    def handle_request(self, conn, *args):
        """
        Gateway Method for processing each request by its request code.
        """
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
            return self.handle_general_errors(err)
        return 0
