# Flutter + WebSock = :heart:

## Code
### Flutter Dart code
```
import 'package:web_socket_channel/io.dart';

void main() async {

  var channel = IOWebSocketChannel.connect("ws://<YOUR-IP>:8467");
  channel.sink.add("Echo Server");
  channel.stream.listen((message) {
    print(message);
  });
}
```
To test the flutter application in an emulator you need to fill in your IP address.   
It should look something like: 192.168.XX.XX or you use the flutter emulator loopback address: 10.0.2.2.

### WebSock code
```
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
```
To use the WebSock library you need to bind the IP of your server to your local IP.   
Or just use the "0.0.0.0".

## Output
### Flutter Console
```
Echo Client
```

### WebSock Console
```
Connected
Echo Server
```

### Flutter array payload
To send array data between WebSock and Flutter, you need to serialize the array (list) to a string.   
Example:
```
import 'package:web_socket_channel/io.dart';
import 'dart:convert';

void main() async {

  var channel = IOWebSocketChannel.connect("ws://<YOUR-IP>:8467");
  final payload = List.from(["1","2","3"]);
  final jsonEncoder = JsonEncoder();
  channel.sink.add(jsonEncoder.convert(payload));
  channel.stream.listen((message) {
    print(message);
  });
}
```
