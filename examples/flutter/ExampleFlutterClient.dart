import 'package:web_socket_channel/io.dart';

void main() async {

  var channel = new IOWebSocketChannel.connect("ws://192.168.0.38:8467");
  channel.sink.add("Echo Server");
  channel.stream.listen((message) {
    print(message);
  });
}