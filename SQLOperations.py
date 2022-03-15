"""
Class to manage SQL access (data access layer, DAL)
"""
class SQLOperations:


    @staticmethod
    def add_client(user_name,uid,conn,request):
        '''
            For request 110: add a new client (if not exists)
        '''
        cursor = conn.cursor();
        # Refresh cursor to sych mysql:
        cursor.close()
        cursor = conn.cursor()
        public_key = request.getPayloadObject().getContent();
        params = (str(uid),user_name,public_key) # hex(replace(%s,'-',''))uuid)
        cursor.execute(""" INSERT INTO 
                              Clients  
                             (clientId,userName,publicKey,LastSeen) 
                          VALUES 
                             (unhex(replace(%s,'-','')),%s, %s, NOW())""", params);

        conn.commit();
        conn.close;


    @staticmethod
    def get_clients_list(conn):
        '''
            For request 120: provide a list of clients
        '''
        cursor = conn.cursor()
        cursor.execute("""select hex(clientId) clientId, userName 
        from Clients limit 1000 """);
        result = cursor.fetchall()
        conn.close;
        return result;

    def select_public_key(conn,pub_key):
        '''
             For request 130: get public key.
        '''
        cursor = conn.cursor()
        # todo 20/2: Need to read the public key from params!!!
        pub_key_str = '%'+pub_key[:pub_key.index('\0')-1]+'%';
        query = """select PublicKey,hex(clientId) from clients  where hex(clientID) like %s"""#""" select PublicKey,clientId from clients  where clientID = %s; """;
        tpl_params = (pub_key_str,)
        cursor.execute(query,tpl_params)
        result = cursor.fetchall();
        conn.close;
        return result;


    def select_client_messages(conn,request):
        '''
            For Request 140 - fetch messages for the specific user
        '''
        cursor = conn.cursor()
        client_id = request.getClientNameOrId()
        client_id_str = '%' + client_id + '%';
        query =""" select messageID,ToClient,FromClient,Type , Content from Messages  where ToClient like %s limit 1000 """
        tpl_params = (client_id_str,)
        cursor.execute(query,tpl_params)
        result = cursor.fetchall();
        conn.close;
        return result;

    def create_client_message(conn, request):
        '''
            For request 150: add a new message to the message table
        '''
        cursor = conn.cursor()
        from_client = request.getClientNameOrId()
        to_client = request.getPayloadObject().getHeaderParam()
        msg_type = request.getPayloadObject().getMessageType();
        msg = request.getPayloadObject().getContent();
        msg_id = request.getPayloadObject().getMsgId();
        params = (str(msg_id) ,to_client, from_client, msg_type, msg);
        cursor.execute(""" insert into 
                                Messages(messageID,ToClient,FromClient,Type,Content) 
                                  VALUES 
                             (%s,%s, %s, %s, %s) """, params);

        conn.commit();
        conn.close;
        return (to_client,msg_id)
