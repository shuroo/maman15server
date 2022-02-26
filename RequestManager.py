from UUIDProvider import UUIDProvider
from SQLOperations import SQLOperations
from Response import Response
from Response2101 import Response2101
from PayloadResponse import PayloadResponse

class RequestManager:

    def handle_general_errors(self):
        msg = "9000 Error Raised and Sent!!"
        print(msg)
        response = Response("9000",PayloadResponse("",msg))
        reply = response.pack_response()
        return reply;

    def handle_create_client_request(self,conn, request):
        print("reached handle_create_client_request!!!!")
        ident = UUIDProvider.createUniqueID()
        SQLOperations.add_client(request.getClientName(), ident, conn, request)
        response = Response("2100", PayloadResponse(ident))
        reply = response.pack_response()
        return reply;

    # For Request 120:
    def handle_clients_list_request(self,conn, *args):
        clients_list = SQLOperations.get_clients_list(conn);
        response = Response2101(clients_list)
        reply = response.pack_response()
        return reply;

    # For Request 130:
    def handle_public_key_request(self,conn, request130):
        print("reached handle_public_key_request!!!!")
        pub_key = SQLOperations.select_public_key(conn,request130.getClientId());
        response = Response("2102", PayloadResponse("",pub_key))
        reply = response.pack_response()
        return reply;
    #
    # # For Request 140:
    # def handle_get_client_messages_request(self,conn, *args):
    #     print("reached handle_get_client_messages_request!!!!")
    #     messages = SQLOperations.select_client_messages(conn,args);
    #     return messages;
    #
    # # For Request 150:
    # def handle_create_message_request(self,conn, *args):
    #     print("reached handle_create_message_request!!!!")
    #     messages = SQLOperations.create_client_message(conn,args);
    #     return messages;

    # TBD: Requests: 150,151,152,153,0

    def handle_request(self, conn, *args):
        try:
            request = args[0];
            request_code = request.getRequestCode();
            # 110 - register: - reply should be 2100 when ok or 9000 - otherwise
            if request_code == "1100":
                pubKey = self.handle_create_client_request(conn,*args);
                return pubKey;
            # 120 - clients list: - reply should be __ when ok or 9000 - otherwise
            if request_code == "1101":
                clients_list = self.handle_clients_list_request(conn,*args);
                return clients_list;
            # 130 - clients list: - reply should be __ when ok or 9000 - otherwise
            if request_code == "1102":
                pubKey = self.handle_public_key_request(conn,*args);
                return pubKey;
            # 150 - clients list: - reply should be __ when ok or 9000 - otherwise
            if request_code == "1104":
                pubKey = self.handle_get_client_messages_request(conn,*args);
                return pubKey;
            # 140 - clients list: - reply should be __ when ok or 9000 - otherwise
            if request_code == "1103":
                pubKey = self.handle_create_message_request(conn,*args);
                return pubKey;

            # if request_code == "151":
            #     pubKey = self.handle_request_for_symmetric_key(conn,*args);
            #     return pubKey;
            #
            # if request_code == "152":
            #     pubKey = self.handle_create_client_request(conn,*args);
            #     return pubKey;
        except Exception as err:
            print('Failed to handle request. Error raised:', err);
            return self.handle_general_errors()
        return 0
