# WebSock

[![PyPI](https://img.shields.io/pypi/v/websock.svg)](https://pypi.org/project/websock/)
[![Build Status](https://travis-ci.org/Kai-Bailey/WebSock.svg?branch=master)](https://travis-ci.org/Kai-Bailey/WebSock)

<img src="logo/WebSock.JPG" width="60%">

A lightweight, multithreaded WebSocket server written in Python.  

## Example Use Case - Chat Application

To demonstrate one use case for WebSock, an online chat application has been set up [here](http://websock-chat.ml/). The application's backend server is built on top of WebSock and is deployed within a Docker container hosted by Digital Ocean. The code for the chat application is provided within the [examples directory](https://github.com/Kai-Bailey/WebSock/tree/master/examples).

## Description

WebSock is a Python implementation of a WebSocket server. WebSock allows you to create real-time applications, such as chatrooms or stock dashboards, without having to implement all the low-level details specified in the WebSocket protocol. The server application is built using the [TCP socket module](https://docs.python.org/3/howto/sockets.html) provided by the Python programming language and follows the latest version of the WebSocket protocol specification ([RFC 6455](https://datatracker.ietf.org/doc/rfc6455/)). The project was motivated by our desire to learn more about how data is transferred across networks while providing a useful tool for others to build on top of.

## Design
WebSock is an abstraction that hides the unnecessary complexities of the WebSocket protocol and provides a simple API that allows users to get their applications up and running quickly. The server listens for new client connections on its main application thread while offloading the management of individual client interactions to a dedicated client thread -- creating a new thread for each client connection.  Client threads are created the moment an upgrade request is received and are destroyed following the transmission of the final close frame. This design allows the server to manage multiple clients concurrently without the concern of a non-responding client blocking the transmission of data to/from other clients.

## How to Run

Install the library by executing:

```python
pip install websock
```

WebSock's API is easy to integrate into any application. To use the server you must provide an implementation for any or all of the following methods:

```python
def on_data_receive(client, data):
    '''Called by the WebSocket server when data is received.'''
    # Your implementation here.

def on_connection_open(client):
    '''Called by the WebSocket server when a new connection is opened.'''
    # Your implementation here.
    
def on_error(exception):
    '''Called by the WebSocket server whenever an Exception is thrown.'''
    # Your implementation here.
    
def on_connection_close(client):
    '''Called by the WebSocket server when a connection is closed.'''
    # Your implementation here.

def on_server_destruct():
    '''Called immediately prior to the WebSocket server shutting down.'''
    # Your implementation here.
```

Then, simply import and instantiate a new WebSocketServer object. The server expects a host and port, as well as any combination of the above methods.

```python
from websock import WebSocketServer

my_server = WebSocketServer(
    "127.0.0.1",        # Example host.
    8467,               # Example port.
    on_data_receive     = on_data_receive,
    on_connection_open  = on_connection_open,
    on_error            = on_error,
    on_connection_close = on_connection_close,
    on_server_destruct  = on_server_destruct
)

my_server.serve_forever()
```

For more guidance, check out the code for the example chat application built using WebSock in the [examples directory](https://github.com/Kai-Bailey/WebSock/tree/master/examples).
## API Documentation
You can check out the full documentation for the API [here](https://websock.readthedocs.io/en/latest/).

## Authors
* [Kai Bailey](https://github.com/Kai-Bailey) - Software engineering student at the University of Alberta.
* [Fraser Bulbuc](https://github.com/fbulbuc) - Software engineering student at the University of Alberta.

## References
* The latest official WebSocket protocol specification, [RFC 6455](https://datatracker.ietf.org/doc/rfc6455/).
* Mozilla has an abundance of information on web technologies including a section on [WebSockets](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API).
* A chat bot, built using [ChatterBot](https://github.com/gunthercox/ChatterBot), was added to the example chat application so that the chat room is never empty!

## Future Development

* Integration of the [Autobahn test suite](https://github.com/crossbario/autobahn-testsuite) to verify protocol coverage.
