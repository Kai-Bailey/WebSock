import socket
import threading
import hashlib
import base64


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
                resp = (True, (WebSocketServer._HANDKSHAKE_RESP % (digest)).encode())
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
    def _decode_dataframe(data):
        """Decodes a data frame formatted as per RFC 6455.

        :param data: The raw data frame.

        :returns: A String of the payload or None if the format could not be understood.
        """
        pass

    @staticmethod
    def _encode_dataframe(data):
        """Formats data into a data frame as per RFC 6455.

        :param data: The data to be formatted.

        :returns: The formatted data.
        """
        pass

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


class WS_FRAME_FORMAT:

    """ Contains information about the format of the data frames. 

    The following keys hold information about the format of each 
    field:
        'LABEL'      - Returns the field name as a String.
        'START_BIT'  - Returns the index of the first bit for the field.
        'BIT_LENGTH' - Returns the number of bits in the field.

        0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
        +-+-+-+-+-------+-+-------------+-------------------------------+
        |F|R|R|R| opcode|M| Payload len |    Extended payload length    |
        |I|S|S|S|  (4)  |A|     (7)     |             (16/64)           |
        |N|V|V|V|       |S|             |   (if payload len==126/127)   |
        | |1|2|3|       |K|             |                               |
        +-+-+-+-+-------+-+-------------+ - - - - - - - - - - - - - - - +
        |     Extended payload length continued, if payload len == 127  |
        + - - - - - - - - - - - - - - - +-------------------------------+
        |                               |Masking-key, if MASK set to 1  |
        +-------------------------------+-------------------------------+
        | Masking-key (continued)       |          Payload Data         |
        +-------------------------------- - - - - - - - - - - - - - - - +
        :                     Payload Data continued ...                :
        + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
        |                     Payload Data continued ...                |
        +---------------------------------------------------------------+
    """

    FIN = {
        'LABEL': "Fin",
        'START_BIT': 0,
        'BIT_LENGTH': 1
    }

    MASK = {
        'LABEL': "Mask",
        'START_BIT': 8,
        'BIT_LENGTH': 1
    }

    OPCODE = {
        'LABEL': "OpCode",
        'START_BIT': 4,
        'BIT_LENGTH': 4
    }

    PAYLOAD_LEN = {
        'LABEL': "Payload Length",
        'START_BIT': 9,
        'BIT_LENGTH': 7
    }

    PAYLOAD_LEN_EXT_126 = {
        'LABEL': "Extended Payload Length (126)",
        'START_BIT': 16,
        'BIT_LENGTH': 16
    }

    PAYLOAD_LEN_EXT_127 = {
        'LABEL': "Extended Payload Length (127)",
        'START_BIT': 16,
        'BIT_LENGTH': 64
    }

    MASK_KEY = {
        'LABEL': "Masking Key",
        'START_BIT': 79,
        'BIT_LENGTH': 32
    }

    PAYLOAD = {
        'LABEL': "Payload",
        'START_BIT': 111,
        'BIT_LENGTH': -1 # Payload length must be read from the PAYLOAD_LEN field.
    }
