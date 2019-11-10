import threading
from websock.WebSocketServer import WebSocketServer

server = WebSocketServer("127.0.0.1", 9010)
server_thread = threading.Thread(target=server.serve_forever(), args=(), daemon=True)
server_thread.start()

print('Started')