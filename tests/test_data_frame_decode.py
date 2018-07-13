import unittest
import sys
import os

proj_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
socket_folder = os.path.join(proj_folder, 'websocket')
sys.path.insert(0, socket_folder)

import WebSocketServer as WS


class TestDataFrameDecode(unittest.TestCase):

    def test_decode(self):
        """Test that data frames are decoded properly."""
        pass


if __name__ == "__main__":
    unittest.main()
