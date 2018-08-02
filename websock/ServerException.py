class WebSocketInvalidHandshake(Exception):
    """ The client and server were unable to complete the handshake protocol
    """

    def __init__(self, message, client):
        super().__init__(message)
        self.client = client


class WebSocketInvalidDataFrame(Exception):
    """ The server was unable to parse the data frame
    """

    def __init__(self, message, client):
        super().__init__(message)
        self.client = client