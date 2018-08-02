import socket
import threading
import hashlib
import base64
import logging
from .DataFrameFormat import *
from .ServerException import *

class WebSocketServer():

    _SEC_KEY = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    _HANDKSHAKE_RESP = (
        "HTTP/1.1 101 Switching Protocols\r\n"
        "Upgrade: websocket\r\n"
        "Connection: Upgrade\r\n"
        "Sec-WebSocket-Accept: %s\r\n\r\n"
    )

    _LOGS_FILE = "ws.log"
    _LOG_IN = "[IN] "
    _LOG_OUT = "[OUT]"

    def __init__(self, ip, port, on_data_receive=None, on_connection_open=None, on_connection_close=None, on_server_destruct=None, on_error=None, DEBUG=False):
        self.server = None
        self.ip = ip
        self.port = port
        self.alive = True
        self.clients = {}   # Dictionary of active clients, remove when the connection is closed.
        self.on_data_receive = on_data_receive if on_data_receive != None else self._default_func
        self.on_connection_open = on_connection_open if on_connection_open != None else self._default_func
        self.on_connection_close = on_connection_close if on_connection_close != None else self._default_func
        self.on_server_destruct = on_server_destruct if on_server_destruct != None else self._default_func
        self.on_error = on_error if on_error != None else self._default_func
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.DEBUG = DEBUG

        # Initialize log file format.
        logging.basicConfig(
            filename=WebSocketServer._LOGS_FILE,
            filemode='w',
            format='%(levelname)s:%(threadName)s\n\t%(message)s',
            level=logging.DEBUG if DEBUG else logging.INFO
        )

    def _default_func(self, *args, **kwargs):
        """Default function if the user does not define one.
        """
        pass

    def serve_forever(self):
        """Just like serve_once but forever.
        """
        self.server.bind((self.ip, self.port))
        self.server.listen(5)
        while self.alive:
            self.serve_once(serve_forever=True)

    def serve_once(self, serve_forever=False):
        """Listen for incoming connections and start a new thread if a client is received.
        """

        if not serve_forever:
            self.server.bind((self.ip, self.port))
            self.server.listen(5)

        logging.info("Server is ready to accept")
        client, addr = self.server.accept()
        self.clients[addr] = client
        logging.info("{} CONNECTION: {}".format(WebSocketServer._LOG_IN, client.getsockname()))

        if serve_forever:
            client_thread = threading.Thread(target=self._manage_client, args=(client,), daemon=True)
            client_thread.start()
        else:
            self._manage_client(client)


    def _manage_client(self, client):
        """This function is run on a separate thread for each client. It will complete the opening handshake 
            and then listen for incoming messages executing the users defined functions. The thread will close
            when this function returns.

        :param client: The client to control
        """   
        upgrade_req = client.recv(2048)
        valid, ack = self._opening_handshake(client, upgrade_req)

        if valid:
            client.send(ack)
        else:
            self.on_error(WebSocketInvalidHandshake("Invalid Handshake", client))            

        self.on_connection_open(client)

        address = client.getpeername()
        while address in self.clients:
            self._recv(client)


    def recv(self, client):
        """Receive data from the client. This function will not call the user defined on_data_receive
           but will instead return the data. If a the next message from the client is not data (for example a close
           request) that message will be handled and none will be returned. This thread will be blocked until a
           message is received.
        
            :param client: The client to receive a message from.
            :returns: The message sent by the client.
        """
        return self._recv(client, user=True)

    def _recv(self, client, user=False):
        """Receive a message from the client. Will block this thread until a message is received.
        
            :param client: The client to receive a message from.
        """
        address = client.getpeername()    
        data = client.recv(2048)
        
        try:
            valid, data = self._decode_data_frame(data)
        except:
            valid = None
         
        if valid == FrameType.TEXT:
            logging.info("{} {}: {} - '{}'".format(WebSocketServer._LOG_IN, valid.name, client.getsockname(), data))
            if user:
                return data
            else:
                self.on_data_receive(client, data)
        elif valid == FrameType.CLOSE:
            logging.info("{} {}: {}".format(WebSocketServer._LOG_IN, valid.name, client.getsockname()))
            
            # Server sent closing message client connection has already closed
            if not self.clients[address]:
                self.close_client(client)

        elif valid == FrameType.PING:
            logging.info("{} {}: {}".format(WebSocketServer._LOG_IN, valid.name, client.getsockname()))
            self._pong(client)
        elif valid == FrameType.PONG:
            logging.info("{} {}: {}".format(WebSocketServer._LOG_IN, valid.name, client.getsockname()))
        else:
            self.on_error(WebSocketInvalidDataFrame("Recieved Invalid Data Frame", client))

    def send(self, client, data, data_type=FrameType.TEXT):
        """Send a string of data to the client.

        :param data: The data to send.
        :param client: The Client to send the data too.
        :param data_type: The FrameType -- assumed to be a utf-8 encoded String if left out.
        """ 
        logging.info("{} {}: {} - '{}'".format(WebSocketServer._LOG_OUT,
                                               data_type.name, client.getsockname(), data if data else ''))
        data = WebSocketServer._encode_data_frame(data_type, data)
        client.send(data)

    def send_all(self, client, data, echo=False):
        """Send a string of data to all clients.

        :param data: A string of data formatted as ASCII
        :param client: The client initiating the data transfer.
        :param echo: A boolean that indicates whether 'client' 
        should receive an echo of the message they are initiating.
        """
        for endpoint in self.clients.values():
            if endpoint != client or echo:
                self.send(endpoint, data)

    def _opening_handshake(self, client, data):
        """Derives handshake response to a client upgrade request.

        :param client: The client to complete the handshake with.
        :param data: The raw data included in the upgrade request -- assumes
        the input data is encoded in a utf-8 format.

        :returns (valid, response): A tuple containing a boolean flag 
        indicating if the request was valid, and a String containing
        the handshake response (encoded in utf-8 format) or None if 
        the upgrade request was invalid.
        """
        resp = (False, None)
        tokens = data.decode().split("\r\n")

        if "Upgrade: websocket" not in tokens or "Connection: Upgrade" not in tokens:
            return resp

        for token in tokens[1:]:
            label, value = token.split(": ", 1)
            if label == "Sec-WebSocket-Key":
                digest = WebSocketServer._digest(value)
                resp = (True, (WebSocketServer._HANDKSHAKE_RESP %
                               (digest)).encode())
                break

        return resp

    @staticmethod
    def _digest(sec_key):
        """Derives the Sec-Accept key from the client's Sec-Key.

        :param sec_key: A String representing the Sec-Key provided in an upgrade request.

        :returns: A utf-8 encoding of the Sec-Accept key.
        """
        raw = sec_key + WebSocketServer._SEC_KEY
        return base64.b64encode(hashlib.sha1(raw.encode("ascii")).digest()).decode("utf-8")

    @staticmethod
    def _decode_data_frame(data):
        """Decodes a data frame formatted as per RFC 6455.

        :param data: The incoming byte string.
 
        :returns: A tuple of (FrameType, String) where the FrameType will be None
        if the data could not be understood.
        """
        fin = (data[FIN[LOW]]&FIN[BIT_MASK])>>FIN[OFFSET]
        opcode = (data[OPCODE[LOW]]&OPCODE[BIT_MASK])>>OPCODE[OFFSET]

        # Check that the payload is valid.
        frame_type = [f_type for f_type in FrameType if opcode == f_type]
        if not frame_type:
            return (None, None)
        else:
            frame_type = frame_type[0]

        mask_key_low = PAYLOAD_LEN[HIGH]+1
        payload_len = (data[PAYLOAD_LEN[LOW]]&PAYLOAD_LEN[BIT_MASK])>>PAYLOAD_LEN[OFFSET]
        if payload_len == 126:
            # Read the next 16 bits.
            mask_key_low = PAYLOAD_LEN_EXT_126[HIGH]+1
            payload_len = int.from_bytes(data[PAYLOAD_LEN_EXT_126[LOW] : PAYLOAD_LEN_EXT_126[HIGH]+1],'big')
        elif payload_len == 127:
            # Read the next 64 bits.
            mask_key_low = PAYLOAD_LEN_EXT_127[HIGH]+1
            payload_len = int.from_bytes(data[PAYLOAD_LEN_EXT_127[LOW] : PAYLOAD_LEN_EXT_127[HIGH]+1],'big')

        mask = (data[MASK[LOW]]&MASK[BIT_MASK])>>MASK[OFFSET]
        mask_key_high = mask_key_low + MASK_KEY[LEN] if mask else mask_key_low
        mask_key = payload = None

        if mask: # Need to unmask the payload data.
            mask_key = data[mask_key_low: mask_key_high]
            encrypted = data[mask_key_high: mask_key_high+payload_len]
            payload = bytearray(encrypted[i]^mask_key[i%4] for i in range(len(encrypted)))
        else:
            payload = data[mask_key_high: mask_key_high+payload_len]

        return (frame_type, bytes(payload).decode() if frame_type != FrameType.CLOSE else None)


    @staticmethod
    def _encode_data_frame(frame_type, data):
        """Formats data into a data frame as per RFC 6455.

        :param frame_type: FrameType indicating the type of data being sent.
        :param data: The data to be formatted.

        :returns: The formatted data frame.
        """
        data = data.encode() if data else None

        fin = 1  # No fragmentation support yet.
        mask = 0 # Server never masks data.
        opcode = frame_type.value

        # Create the data frame one byte at a time.
        frame = bytearray()
        frame.append((fin<<FIN[OFFSET])^opcode)

        payload_len = len(data) if data else 0
        if payload_len < 126:
            frame.append((mask<<MASK[OFFSET])^payload_len)
        elif payload_len < 65535 : # Can the length fit in 16 bits?
            frame.append((mask<<MASK[OFFSET])^126)
            for i in range(PAYLOAD_LEN_EXT_126[LEN]-1,-1,-1):
                frame.append((payload_len>>(i*8))&255)
        else:
            frame.append((mask<<MASK[OFFSET])^127)
            for i in range(PAYLOAD_LEN_EXT_127[LEN]-1,-1,-1):
                frame.append((payload_len>>(i*8))&255)
        
        if payload_len > 0:
            frame.extend(data)    
        return bytes(frame)

    def _initiate_close(self, client, status_code=None, app_data=None):
        """Sends the first Closing frame to the client.

        :param client: The Client connection to close.
        :param status_code: A 16 bit optional status code.
        :param app_data: A utf-8 encoded String to include with the close frame.
        """
        # Concatenate the status_code and app_data into one byte string if provided.
        payload_bytes = []
        if status_code is not None:
            status_bytes = bytearray([status_code & 255, (status_code >> 8) & 255])
            payload_bytes.append(bytes(status_bytes))

        if app_data is not None:
            payload_bytes.append(app_data.encode())

        self.send(client, b''.join(payload_bytes) if len(payload_bytes) > 0 else None, FrameType.CLOSE)

    def _respond_to_close(self, client):
        """Acknowledge the closing of a client connection -- for now, just send an empty
        close frame (i.e. same as initiating a close frame with no app_data). Later, this
        will be udpated to echo the status_code from the client's close frame.

        :param client: The Client who requested the connection close.
        """
        self._initiate_close(client)

    def close_client(self, client, status_code=None, app_data=None):
        """Close the connection with a client.

        :param client: The client to close the connection with.
        :param status_code: A 16 bit optional status code.
        :param app_data: A utf-8 encoded String to include with the close frame.
        """
        self.on_connection_close(client)
        self._initiate_close(client, status_code=status_code, app_data=app_data)
        self.clients.pop(client.getpeername(), None)
        client.close()

    def close_server(self, status_code=None, app_data=None):
        """Close the connection with each client and then close the underlying tcp socket of the server.
        
        :param status_code: A 16 bit optional status code to send to all of the clients.
        :param app_data: A utf-8 encoded String to include with the close frame.
        """

        for client in list(self.clients.values()):
            self.close_client(client, status_code=status_code, app_data=app_data)

        self.on_server_destruct()
        self.server.close()
        self.alive = False

    def ping(self, client):
        """Send a Ping frame.

        :param client: The Client to ping."""
        self.send(client, None, FrameType.PING)

    def _pong(self, client):
        """Send a Pong frame back to a client.

        :param client: The Client who send the Ping.
        """
        self.send(client, None, FrameType.PONG)
