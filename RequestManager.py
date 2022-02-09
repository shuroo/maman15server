from UUIDProvider import UUIDProvider
from SQLOperations import SQLOperations
from Response import Response
from Payload import Payload

class RequestManager:

    def handle_general_errors(self):
        print("9000 Error Raised and Sent!!")
        response = Response("9000")
        reply = response.pack_response()
        return reply;

    def handle_create_client_request(self,conn, request):
        print("reached handle_create_client_request!!!!")
        ident = UUIDProvider.createUniqueID();
        SQLOperations.add_client(request.getClientName(), ident, conn, request);
        response = Response("2100", Payload(ident))
        reply = response.pack_response()
        return reply;

    # bytes.fromhex(response.getClientID())
    # resp_size = struct.calcsize(struct.pack(response))
    # response = struct.pack(Response("","", ident, Constants.version, "2100" ,
    #          resp_size, 0, ""))

    # For Request 120:
    def handle_clients_list_request(self,conn, *args):
        print("reached handle_clients_list_request!!!!")
        clients_list = SQLOperations.get_clients_list(conn);
        return clients_list;

    # For Request 130:
    def handle_public_key_request(self,conn, *args):
        print("reached handle_public_key_request!!!!")
        pub_key = SQLOperations.select_public_key(conn,args);
        return pub_key;

    # For Request 140:
    def handle_get_client_messages_request(self,conn, *args):
        print("reached handle_get_client_messages_request!!!!")
        messages = SQLOperations.select_client_messages(conn,args);
        return messages;

    # For Request 150:
    def handle_create_message_request(self,conn, *args):
        print("reached handle_create_message_request!!!!")
        messages = SQLOperations.create_client_message(conn,args);
        return messages;

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
                pubKey = self.handle_clients_list_request(conn,*args);
                return pubKey;
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
            print('Failed to handle request. error raised:\n', err);
            return self.handle_general_errors()
        return 0
