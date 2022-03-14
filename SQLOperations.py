from UUIDProvider import UUIDProvider;

class SQLOperations:

#### TODO : FINISH THIS!! ####

    '''
        For request 110: add a new client (if not exists)
    '''
    @staticmethod
    def add_client(user_name,uid,conn,request):

        cursor = conn.cursor();
        # Refresh cursor to sych mysql:
        cursor.close()
        cursor = conn.cursor()
        public_key = request.getPayloadObject().getContent();
        print('uid given to new user is:',uid)
        params = (str(uid),user_name,public_key) # hex(replace(%s,'-',''))uuid)
        print("username request 110:",user_name)
        cursor.execute(""" INSERT INTO 
                              Clients  
                             (clientId,userName,publicKey,LastSeen) 
                          VALUES 
                             (unhex(replace(%s,'-','')),%s, %s, NOW())""", params);
        #  (unhex(replace('%s','-','')),'%s', '%s', NOW());
        conn.commit();
        conn.close;

    '''
        For request 120: provide a list of clients 
    '''
    @staticmethod
    def get_clients_list(conn):
        cursor = conn.cursor()
        cursor.execute("""select hex(clientId) clientId, userName 
        from Clients limit 1000 """); # LPAD(, 16, '\0') , CAST(clientId as CHAR(16))
        # select hex(clientId),publicKey from clients  where hex(clientId) = 'AC30F66482304F4C8ECB290C85E2BFE9';
        result = cursor.fetchall();
        print('client ids fetched:::',result)
        conn.close;
        return result;

    '''
        For request 130: get public key by client 
    '''
    def select_public_key(conn,pub_key):
        cursor = conn.cursor()
        # todo 20/2: Need to read the public key from params!!!
        print("pub_key before select 2101:",pub_key);
        pub_key_str = '%'+pub_key[:pub_key.index('\0')-1]+'%';
        query = """select PublicKey,hex(clientId) from clients  where hex(clientID) like %s"""#""" select PublicKey,clientId from clients  where clientID = %s; """;
        tpl_params = (pub_key_str,)
        cursor.execute(query,tpl_params)
        result = cursor.fetchall();
        conn.close;
        return result;


    '''
        For Request 140
    '''

    def select_client_messages(conn,request):
        cursor = conn.cursor()
        client_id = request.getClientNameOrId()
        cursor.execute(""" select * from Messages  limit 1000; """) #where ToClient = %s,client_id)
        result = cursor.fetchall();
        conn.close;
        return result;



    '''
        For request 150: add a new message
        TODO: how to return failure status?
    '''

    def create_client_message(conn, request):
        cursor = conn.cursor()
        from_client = request.getClientNameOrId()
        to_client = request.getPayloadObject().getHeaderParam()
        msg_type = request.getPayloadObject().getMessageType();
        # todo: decrypt the encrypted msg??
        msg = request.getPayloadObject().getContent();
        msg_id = request.getPayloadObject().getMsgId();
        # TODO: What is this?
        params = (msg_id ,to_client, from_client, msg_type, msg);
        cursor.execute(""" insert into 
                                Messages(messageID,ToClient,FromClient,Type,Content) 
                                  VALUES 
                              (unhex(replace(%s,'-','')),%s, %s, %s, %s) """, params);
        conn.commit();
        conn.close;
        return (to_client,msg_id)
