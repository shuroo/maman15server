
import selectors
import socket
import struct
from Request import Request
from Payload import Payload
from RequestManager import RequestManager
from SQLInitiator import SQLInitiator
from Constants import Constants
from MsgPayload import MsgPayload

sel = selectors.DefaultSelector()


def accept(sock, mask):
     conn, addr = sock.accept() # Should be ready
     print('accepted', conn, 'from', addr)
     conn.setblocking(False)
     sel.register(conn, selectors.EVENT_READ, parse_request)


def build_request(data):
    #todo: header param should be client id..
    client_id = '' # optional name or key...
    req_code = struct.unpack("<H", data[:2])[0];
    version = struct.unpack("<B", data[2:3])[0];
    payload_size = struct.unpack("<I", data[6:10])[0];
    if req_code != 1100 :
        # 16byte =128bit = 128+nullTerm = 129 = len(clientId)
        client_id = struct.unpack("<17s", data[10:27])[0].decode("utf-8");
    ## todo: should be 4 bits long
    if payload_size == 0:
        payload = ""
    else:
        ## todo: try catch for the other params as well.!!!
        try:
            start_index_payload = 27
            # todo: parse payload and pass as a string on the client side.
            payload_data = struct.unpack("<%ds" % payload_size, data[start_index_payload:start_index_payload+payload_size])[0];
            payload = build_payload(payload_data,req_code);
            client_id = payload.getHeaderParam();
        except Exception as e:
            print("Failed to parse payload, error:",e);
            payload = "";
    params = Request(client_id, version, req_code, payload_size, client_id, payload);
    return params;

# buffer payload:
# b'\x00\x08\x00\x00\x00bl\x00\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe'
def build_payload(data,resp_code):
    if resp_code == 1102 :
       # pl_sze = struct.unpack("<I", data[:4])
       # todo: need to be 16 bits. FIX!
        client_id = struct.unpack("<%dp"% len(data[:46]), data[:46])[0].decode('utf-8') # [15:62]
        return Payload(client_id);
    if resp_code == 1103 :
        print("data:",data)
        # todo: need to be 16 bits. FIX!
        client_id = struct.unpack("<%dp"% len(data[:17]), data[:17])[0].decode('utf-8')
        msg_type = struct.unpack("<c", data[18:19])[0].decode('utf-8')
        msg_content = struct.unpack("<%dp"% len(data[19:23]), data[19:23])[0].decode('utf-8')
        pl_size = struct.unpack("<4s", data[23:27])[0].decode('utf-8')
        content_sz = struct.unpack("<4s", data[27:31])[0].decode('utf-8')
        return MsgPayload(client_id,msg_type, content_sz, msg_content); # client_id,msg_type, content_sz=0, msg_content=""
    else:
        # todo: what about the first 3 bits?--it is uint32 -size!!
        # case for request 110, and..?
        name_or_message = struct.unpack("<%ds"% len(data[:256]), data[:256])[0].decode("utf-8") # 256
        public_key = struct.unpack("<%ds"% len(data[256:417]), data[256:417])[0]  # ("<%ds"%(len(data[261:])), data[261:])[0]# 161
        return Payload(name_or_message, public_key);

def fetch_request_params(conn):

    #### Mark this when params are not fetched as string with delimiters:
    #
    # ToDo: Place in constant.
    length = Constants.max_buffer_size; # in bytes;
    data = conn.recv(length);
    print("data:")
    print(data);

    request = build_request(data);
    print("successfully fetched request:",request)
    return request;


def parse_request(conn, mask):
     params = fetch_request_params(conn)
     sql = SQLInitiator();
     sql_conn = sql.cnx;
     req_man = RequestManager();
     resp = req_man.handle_request(sql_conn, params);
     reply = str(resp).encode()
     replydata = bytearray(reply)
     print("Replying with data:", reply)
     conn.send(replydata)# Hope it won't blo


def reply(conn,mask):
    print("Please reply.. ")
    reply = input()
    replydata = bytearray(reply, "utf-8")
    newdata = bytearray(1024)
    for i in range(min(len(replydata), len(newdata))):
        newdata[i] = replydata[i]
    conn.send(newdata)


if __name__ == '__main__':

    #### TBD::: unmark this to match to demo. ####
    #
    #
    # exec(open("SQLInitiator.py").read())
    # params = [b'bababa', '2', '1100']  # fetch_request_params(conn)
    # sql_conn = SQLInitiator.cnx;
    # req_manager = RequestManager();
    # resp = req_manager.handle_request(sql_conn, params);
    # # client list:
    # params = [b'bababa', '2', '1101']
    # resp = req_manager.handle_request(sql_conn, params);
    # params = [b'bababa', '2', '1102']
    # resp = req_manager.handle_request(sql_conn, params);
    # params = [b'bababa', '2', '1103']
    # resp = req_manager.handle_request(sql_conn, params);
    # reply = str(resp).encode();
    # # try:
    # #     sqlConn = SQLInitiator.setSQLEnv();
    # # except:
    # #   print("Failed to init sql env of name:" , sqlConn);

    #### TBD::: unmark this to match to server. ####

    # Read port ...
    f = open("MyPort.info", "r")
    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    PORT = f.read()        # Port to listen on (non-privileged ports are > 1023)

    try:
        # Reset DB:
        sql = SQLInitiator();
        conn = sql.setSQLEnv();
        PORT = int(PORT)
        # Connect via socket.
        sock = socket.socket()
        sock.bind((HOST, PORT))
        sock.listen(100)
        sock.setblocking(False)
        sel.register(sock, selectors.EVENT_READ, accept)

        while True:
         events = sel.select()
         for key, mask in events:
            callback = key.data
            print(key.data)
            callback(key.fileobj, mask)
    except Exception as e:
      print("Error connecting to socket. aborting. error:", e)
