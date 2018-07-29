"""
Example of a chat server. Users first select a username and then can chat using the following format.
Send a message to a specific user
username:message

Send a message to everyone
all:message

send a message to the chatbot
chatbot:message

Disconnect from the chat server
disconnect
"""
import os
import sys

proj_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
socket_folder = os.path.join(proj_folder, 'websocket')
sys.path.insert(0, socket_folder)

import WebSocketServer
from chatterbot import ChatBot

URL = "127.0.0.1"
PORT = 8467

def on_data_receive(client, data):
    """Called by the WebSocketServer when data is received."""

    #Process Message
    message = data.split(":")
    username = message[0]
    message = ":".join(message[1:])

    if username == "disconnect":
        server.close_client(client)
    elif username == "all":
        server.send_all(client, message)
    # elif username == "chatbot":
    #     chatbotResponse = chatbot.get_response(message)
    #     server.send(client, chatbotResponse)
    else:
        if username in usernames_to_ip:
            client_ip = usernames_to_ip[username]
            client_to_send = users[client_ip].client_socket
            server.send(client_to_send, message)
        else:
            server.send(client, "Sorry that user is not online!")
    

def on_connection_open(client):
    """Called by the WebSocketServer when a new connection is opened.
    """
    server.send(client, "Hello Welcome to the Chat Server!\nPlease Enter a username: ")

    ip = client.getpeername()
    users[ip] = User(ip, client)

    # Set the username
    username_invalid = True
    while username_invalid:
        username = server.recv(client)
        if username in usernames_to_ip:
            server.send(client, "Sorry that username is already taken, please try again:")
        else:
            users[ip].username = username
            usernames_to_ip[username] = ip
            server.send(client, "Your username is: " + username)
            username_invalid = False


def on_error(exception):
    """Called when the server returns an error
    """
    raise exception
    
def on_connection_close(client):
    """Called by the WebSocketServer when a connection is closed."""
    server.send(client, "Hope You Enjoyed Chatting!")
    ip = client.getpeername()
    username = users[ip].username
    users.pop(ip)
    usernames_to_ip.pop(username)
    

def on_server_destruct():
    """Called immediately prior to the WebSocketServer shutting down."""
    pass


# chatbot = ChatBot(
#     'chatServer',
#     trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
# )

# # Train based on the english corpus
# chatbot.train("chatterbot.corpus.english")


# Dictionary of users
# Key:(port, address), Value: User class instance
users = {}

# Key:username Value:(port, address)
usernames_to_ip = {}

class User():

    def __init__(self, ip, client_socket, username=None):
        self.ip = ip
        self.port = ip[0]
        self.address = ip[1]
        self.client_socket = client_socket
        self.username = username


server = WebSocketServer.WebSocketServer(URL, PORT, 
                                        on_data_receive=on_data_receive, 
                                        on_connection_open=on_connection_open, 
                                        on_error=on_error, 
                                        on_connection_close=on_connection_close,
                                        on_server_destruct=on_server_destruct)
server.serve_forever()

