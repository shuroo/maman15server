
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
        print('uid:',uid)
        params = (str(uid),user_name,public_key) # hex(replace(%s,'-',''))uuid)
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
        cursor.execute("""select * from Clients limit 1000; """)
        result = cursor.fetchall();
        conn.close;
        return result;

    '''
        For request 130: get public key by client 
    '''
    def select_public_key(conn,args):
        cursor = conn.cursor()
        client_id = args[0][0]
        str_client = client_id.decode("utf-8")
        query = (""" select PublicKey from clients where clientID = '%s'; """%str_client);
        cursor.execute(query)
        result = cursor.fetchall();
        conn.close;
        return result;


    '''
        For Request 140
    '''

    def select_client_messages(conn,args):
        cursor = conn.cursor()
        client_id = args[0][0]
        cursor.execute(""" select * from Messages where ToClient = %s limit 1000; """,client_id)
        result = cursor.fetchall();
        conn.close;
        return result;



    '''
        For request 150: add a new message
        TODO: how to return failure status?
    '''

    def create_client_message(conn, args):
        cursor = conn.cursor();
        # Refresh cursor to sych mysql:
        cursor.close()
        cursor = conn.cursor()
        from_client = args[0][0]
        to_client = args[0][1]
        # TODO: What is this?z
        c_type = 'v'
        content = args[0][2]
        params = (to_client, from_client, c_type, content)
        cursor.execute(""" insert into 
                                Messages(ToClient,FromClient,Type,Content) 
                                  VALUES 
                                       (%s, %s, %s, %s) """, params);
        # values("xxx","xxx","v","sdfsdf sdfsdfs sdfsf sdfsdf sdfsf");
        conn.commit();
        conn.close;

    '''
        For request 151,152,153 ... 
    '''

    #params = ('002', 'CS', 'BG', 'HD1', 'T1', 'C1', 0, 'U')
