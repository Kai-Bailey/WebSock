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
BOT_PREFIX = "@BOT: "

chatbot = ChatBot(
    'chatServer',
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
)


def on_data_receive(client, data):
    """Called by the WebSocketServer when data is received."""
    server.send_all(client, data)
    bot_response = getBotResp(data)
    server.send_all(client, bot_response, echo=True)


def on_connection_open(client):
    """Called by the WebSocketServer when a new connection is opened.
    """
    server.send(client, "Hello, welcome to the chat server!")
    ip = client.getpeername()
    users[ip] = User(ip, client)


def on_error(exception):
    """Called when the server returns an error
    """
    raise exception


def on_connection_close(client):
    """Called by the WebSocketServer when a connection is closed."""
    ip = client.getpeername()
    users.pop(ip)


def on_server_destruct():
    """Called immediately prior to the WebSocketServer shutting down."""
    pass


def getBotResp(msg):
    return BOT_PREFIX + str(chatbot.get_response(msg))


# Dictionary of users
# Key:(port, address), Value: User class instance
users = {}


class User():

    def __init__(self, ip, client_socket):
        self.ip = ip
        self.port = ip[0]
        self.address = ip[1]
        self.client_socket = client_socket


if __name__ == "__main__":

    # Train based on the english corpus
    chatbot.train("chatterbot.corpus.english")

    server = WebSocketServer.WebSocketServer(URL, PORT,
                                             on_data_receive=on_data_receive,
                                             on_connection_open=on_connection_open,
                                             on_error=on_error,
                                             on_connection_close=on_connection_close,
                                             on_server_destruct=on_server_destruct)
    server.serve_forever()
