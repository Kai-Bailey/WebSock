import unittest
import sys
import os

proj_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
socket_folder = os.path.join(proj_folder, 'websocket')
sys.path.insert(0, socket_folder)

import WebSocketServer as WS


class TestHandShake(unittest.TestCase):

    def test_digest(self):
        """Test the calculation of the Accept-Key."""
        client_key = 'dGhlIHNhbXBsZSBub25jZQ=='
        expected = 's3pPLMBiTxaQ9kYGzzhZRbK+xOo='

        result = WS.WebSocketServer._digest(client_key)
        self.assertEqual(expected, result)

    def test_handshake_valid(self):
        """Test the handshake output for a valid upgrade request."""
        upgrade_request = (
            "GET /chat HTTP/1.1\r\n"
            "Host: example.com:8000\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            "Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\n"
            "Sec-WebSocket-Version: 13\r\n\r\n"
        )

        expected_upgrade_response = (
            "HTTP/1.1 101 Switching Protocols\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            "Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=\r\n\r\n"
        )

        ws = WS.WebSocketServer(None, None)

        valid, upgrade_response = ws._opening_handshake(None, upgrade_request)
        self.assertTrue(valid)
        self.assertEqual(expected_upgrade_response, upgrade_response)

    def test_handshake_invalid(self):
        """Test the handshake output for a valid upgrade request."""
        upgrade_request_bad_upgrade = (
            "GET /chat HTTP/1.1\r\n"
            "Host: example.com:8000\r\n"
            "Upgrade: http\r\n"
            "Connection: Upgrade\r\n"
            "Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\n"
            "Sec-WebSocket-Version: 13\r\n\r\n"
        )

        upgrade_request_bad_connection = (
            "GET /chat HTTP/1.1\r\n"
            "Host: example.com:8000\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Maintain\r\n"
            "Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\n"
            "Sec-WebSocket-Version: 13\r\n\r\n"
        )

        ws = WS.WebSocketServer(None, None)

        valid, _ = ws._opening_handshake(
            None, upgrade_request_bad_upgrade)
        self.assertFalse(valid)

        valid, _ = ws._opening_handshake(
            None, upgrade_request_bad_connection)
        self.assertFalse(valid)


if __name__ == "__main__":
    unittest.main()
