import threading
from websock.WebSocketServer import WebSocketServer


def on_connection_open(client):
    """
    Called by the WebSocket server when a new connection is opened.
    """
    print("Connected")


def on_data_receive(client, data):
    """
    Called by the WebSocket server when data is received.
    """
    print(data)
    response = "Echo Client"
    server.send(client, response)


server = WebSocketServer(ip="0.0.0.0", port=8467,
                         on_data_receive=on_data_receive,
                         on_connection_open=on_connection_open)
server_thread = threading.Thread(target=server.serve_forever(), args=(), daemon=True)
server_thread.start()
