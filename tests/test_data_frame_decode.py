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
        encoded_data = b'\x81\x97p\xb4\x99"$\xdc\xf0QP\xdd\xea\x02\x11\x94\xedG\x03\xc0\xb9O\x15\xc7\xeaC\x17\xd1\xb7'
        expected_decoded_data = "This is a test message."

        valid, decoded_data = WS.WebSocketServer._decode_data_frame(encoded_data)
        self.assertTrue(valid is not None)
        self.assertEqual(expected_decoded_data, decoded_data)


if __name__ == "__main__":
    unittest.main()
