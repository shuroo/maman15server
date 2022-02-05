
import selectors
import socket
import struct
from Request import Request
from Payload import Payload
from RequestManager import RequestManager
from SQLInitiator import SQLInitiator

sel = selectors.DefaultSelector()


def accept(sock, mask):
     conn, addr = sock.accept() # Should be ready
     print('accepted', conn, 'from', addr)
     conn.setblocking(False)
     sel.register(conn, selectors.EVENT_READ, parse_request)


def build_request(data):
    client_id = struct.unpack("<16s", data[:16])[0].decode("utf-8");
    req_code = struct.unpack("<4s", data[17:21])[0].decode("utf-8");
    version = struct.unpack("<c", data[22:23])[0].decode("utf-8");
    message_type = struct.unpack("<c", data[23:24])[0].decode("utf-8");
    ## todo: should be 4 bits long
    payload_size = struct.unpack("<I", data[24:28])[0];
    if payload_size == '0':
        payload = ""
    else:
        ## todo: try catch for the other params as well.!!!
        try:
            # todo: parse payload and pass as a string on the client side.
            # WE CURRENTLY USE PERMENANT SIZE INSTEAD OF THE GIVEN... 256+ 161 = 417
            payload_data = struct.unpack("<%ds" % payload_size, data[28:(28+payload_size)])[0];
            payload = build_payload(payload_data);
        except:
            print("Failed to parse payload.");
            payload = "";
    params = Request(client_id, version, req_code, payload_size, message_type, payload);
    return params;

# buffer payload:
# b'\x00\x08\x00\x00\x00bl\x00\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe'
def build_payload(data):
    payload_size = struct.unpack("<I", data[0:4])#data[28:32])[0];
    name_or_message = struct.unpack("<257s", data[4:261])[0].decode("utf-8") # 256
    public_key = struct.unpack("<%ds"%(len(data[261:])), data[261:])[0]# 161
    return Payload(payload_size, name_or_message, public_key);

def fetch_request_params(conn):

    #### Mark this when params are not fetched as string with delimiters:
    #
    # length = 1024
    # text = conn.recv(length)  # Should be ready
    # if text:
    #     print('echoing', repr(text))
    # gvrTxt = struct.unpack("%ds" % length, text)[0]
    # nullTerminatorIndex = gvrTxt.index(b'\x00')
    # content = gvrTxt[:nullTerminatorIndex]
    # params = str(content).split(" ")
    # return params;
    # ToDo: Place in constant.
    length = 1024; # in bytes;
    data = conn.recv(length);
    print("data:")
    print(data);

    request = build_request(data);
    print("successfully fetched request:",request)
    return request;


def parse_request(conn, mask):
     params = fetch_request_params(conn)
     sql = SQLInitiator();
     sql_conn = sql.setSQLEnv();
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
      PORT = int(PORT)
    except:
      print("Failed to convert port to an integer, of value:",PORT)

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
