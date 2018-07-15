
import WebSocketServer

def on_data_receive(client, data):
    """Called by the WebSocketServer when data is received."""

    print(data)
    data += '!'
    ws.send(client, data)

def on_connection_open(client):
    """Called by the WebSocketServer when a new connection is opened.
    """
    pass
    
def on_error(exception):
    """Called when the server returns an error
    """

    print("client:")
    print(exception.client)
    print("exception: ")
    raise exception
    

def on_connection_close(client):
    """Called by the WebSocketServer when a connection is closed."""
    pass

def on_server_destruct():
    """Called immediately prior to the WebSocketServer shutting down."""
    pass

ws = WebSocketServer.WebSocketServer("127.0.0.1", 8467, on_data_receive=on_data_receive, on_connection_open=on_connection_open, on_error=on_error)
ws.serve_forever()

