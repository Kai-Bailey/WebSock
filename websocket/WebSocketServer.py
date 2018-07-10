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
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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

    def _opening_handshake(self, client):
        """Complete opening handshake between the client and the server.

        :param client: The client to complete the handshake with.
        """
        pass

    @staticmethod
    def _digest(sec_key):
        """Concatenates the sec_key with the _SEC_KEY and computes the SHA1 hash.

        :param sec_key: The sec_key provided in the upgrade request by a client.

        :returns: A base64 encoding of the SHA1 digest.
        """
        raw = sec_key + WebSocketServer._SEC_KEY
        return base64.b64encode(hashlib.sha1(raw.encode("ascii")).digest())

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
