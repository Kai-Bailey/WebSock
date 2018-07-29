import os
import sys

proj_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
socket_folder = os.path.join(proj_folder, 'websocket')
sys.path.insert(0, socket_folder)

import WebSocketServer

def on_data_receive(client, data):
    """Called by the WebSocketServer when data is received."""

    if data == "disconnect":
        ws.close_client(client)
    else:
        data += '!'
        ws.send(client, data)

def on_connection_open(client):
    """Called by the WebSocketServer when a new connection is opened.
    """
    ws.send(client, "Welcome to the echo server!")
    
def on_error(exception):
    """Called when the server returns an error
    """
    raise exception
    
def on_connection_close(client):
    """Called by the WebSocketServer when a connection is closed."""
    ws.send(client, "Closing socket")

def on_server_destruct():
    """Called immediately prior to the WebSocketServer shutting down."""
    pass

ws = WebSocketServer.WebSocketServer("127.0.0.1", 8467, 
                                     on_data_receive=on_data_receive,
                                     on_connection_open=on_connection_open, 
                                     on_error=on_error, 
                                     on_connection_close=on_connection_close)
ws.serve_forever()

