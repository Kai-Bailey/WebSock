class ExampleChatServer:

    def __init__(self):
        pass

    def on_data_receive(self):
        """Called by the WebSocketServer when data is received."""
        pass

    def on_connection_open(self):
        """Called by the WebSocketServer when a new connection is opened."""
        pass

    def on_connection_close(self):
        """Called by the WebSocketServer when a connection is closed."""
        pass

    def on_server_destruct(self):
        """Called immediately prior to the WebSocketServer shutting down."""
        pass
