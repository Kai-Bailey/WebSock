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
        expected = b's3pPLMBiTxaQ9kYGzzhZRbK+xOo='
        result = WS.WebSocketServer._digest(client_key)
        self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main()
