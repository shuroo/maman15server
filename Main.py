
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
    #todo: put unpack in pack utils...
    client_id = '' # optional name or key...
    req_code = struct.unpack("<H", data[:2])[0];
    version = struct.unpack("<B", data[2:3])[0];
    payload_size = struct.unpack("<I", data[6:10])[0];
    if req_code != 1100 :
        # 16byte =128bit = 128+nullTerm = 129 = len(clientId)
        client_id = struct.unpack("<16s", data[10:26])[0].decode("utf-8");
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
    params = Request(client_id, version, req_code, payload_size, payload);
    return params;


def build_payload(data,resp_code):
    if resp_code == 1102 :
       # pl_sze = struct.unpack("<I", data[:4])
       # todo: need to be 16 bits. FIX!
        client_id = struct.unpack("<%dp"% len(data[:46]), data[:46])[0].decode('utf-8') # [15:62]
        return Payload(client_id);
    if resp_code == 1103 :
        print("data in payload:",data)
        # todo: need to be 16 bits. FIX!
        client_id = struct.unpack("<%dp"% len(data[:16]), data[:16])[0].decode('utf-8')
        msg_type = struct.unpack("<c", data[18:19])[0].decode('utf-8')
        content_sz = struct.unpack("<I", data[19:23])[0]
        msg_content = struct.unpack("<%ds"% len(data[23:23+content_sz]), data[23:23+content_sz])[0].decode('utf-8')
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
     request = fetch_request_params(conn)
     sql = SQLInitiator();
     sql_conn = sql.cnx;
     req_man = RequestManager();
     resp = req_man.handle_request(sql_conn, request);
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
    # Read port ...
    f = open("MyPort.info", "r")
    HOST = '127.0.0.1'
    PORT = f.read()

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
