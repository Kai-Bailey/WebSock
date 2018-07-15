import socket
import threading
import hashlib
import base64
from DataFrameFormat import *


class WebSocketServer():

    _SEC_KEY = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    _HANDKSHAKE_RESP = (
        "HTTP/1.1 101 Switching Protocols\r\n"
        "Upgrade: websocket\r\n"
        "Connection: Upgrade\r\n"
        "Sec-WebSocket-Accept: %s\r\n\r\n"
    )

    def __init__(self, ip, port):
        self.server = None
        self.ip = ip
        self.port = port
        self.clients = {}

    def serve(self):
        """Bind server to port and listen for incoming messages.

        """
        self.server.bind((self.ip, self.port))
        self.server.listen(5)

        while True:
            client, addr = self.server.accept()
            self.clients[addr[0]] = client
            threading._start_new_thread(self._opening_handshake, client)

    def send(self, data, client):
        """Send a string of data to the client.

        :param data: A String of data formatted as ASCII.
        :param client: The Client to send the data too.
        """
        pass

    def send_all(self, data):
        """Send a string of data to all clients.

        :param data: A string of data formatted as ASCII
        """

        for client in self.clients:
            self.send(data, client)

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
 
        :returns: A tuple of (boolean, String) where the boolean indicates if 
        the data frame could be understood.
        """
        fin = (data[FIN[LOW]]&FIN[BIT_MASK])>>FIN[OFFSET]
        opcode = (data[OPCODE[LOW]]&OPCODE[BIT_MASK])>>OPCODE[OFFSET]

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

        return (True, bytes(payload).decode())


    @staticmethod
    def _encode_data_frame(data):
        """Formats data into a data frame as per RFC 6455.

        :param data: The data to be formatted.

        :returns: The formatted data frame.
        """
        data = data.encode()
        fin = opcode = 1 # Assumed text data for now.
        mask = 0 # Server never masks data.

        # Create the data frame one byte at a time.
        frame = bytearray()
        frame.append((fin<<FIN[OFFSET])^opcode)

        payload_len = len(data)
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

        frame.extend(data)        
        return bytes(frame)

    def _initiate_close(self, client):
        """Sends the first Closing frame to the client.

        :param client: The Client connection to close.
        """
        pass

    def _respond_to_close(self, client):
        """Acknowledge the closing of a client connection.

        :param client: The Client who requested the connection close.
        """
        pass
