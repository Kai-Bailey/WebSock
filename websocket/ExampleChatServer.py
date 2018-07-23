"""
Example of a chat server. Users first select a username and then can chat using the following format.
Send a message to a specific user
username:message

Send a message to everyone
all:message

Disconnect from the chat server
disconnect
"""

import WebSocketServer

def on_data_receive(client, data):
    """Called by the WebSocketServer when data is received."""
    
    # Set the username
    if users[client.getpeername()][1] == None:
        users[client.getpeername()][1] = data
        usernames_to_client[data] = client
        server.send(client, "Your username is: " + data)
        return

    #Process Message
    message = data.split(":")
    username = message[0]
    message = "".join(message[1:])

    if username == "disconnect":
        server.close_client(client)
    elif username == "all":
        server.send_all(client, message)
    else:
        client_to_send = usernames_to_client[username]
        server.send(client_to_send, message)
    

def on_connection_open(client):
    """Called by the WebSocketServer when a new connection is opened.
    """
    server.send(client, "Hello Welcome to the Chat Server!\nPlease Enter a username: ")
    users[client.getpeername()] = [client, None]

def on_error(exception):
    """Called when the server returns an error
    """
    raise exception
    
def on_connection_close(client):
    """Called by the WebSocketServer when a connection is closed."""
    server.send(client, "Hope You Enjoyed Chatting!")

def on_server_destruct():
    """Called immediately prior to the WebSocketServer shutting down."""
    pass


# Dictionary of users
# Key:(port, address)  Value:(client socket, username)
users = {}

# Key:username Value:client socket
usernames_to_client = {}

server = WebSocketServer.WebSocketServer("127.0.0.1", 8467, 
                                        on_data_receive=on_data_receive, 
                                        on_connection_open=on_connection_open, 
                                        on_error=on_error, 
                                        on_connection_close=on_connection_close,
                                        on_server_destruct=on_server_destruct)
server.serve_forever()

