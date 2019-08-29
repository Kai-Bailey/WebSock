""" Contains information about the format of the data frames. 

The following keys hold information about the format of each 
field:
    'LABEL'      - Returns the field name as a String.
    'BYTE'       - Return the byte number that contains the field.
    'MASK'       - Returns a mask to get the bit.
    'START_BIT'  - Returns the index of the first bit for the field.
    'BIT_LENGTH' - Returns the number of bits in the field.

    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    +-+-+-+-+-------+-+-------------+-------------------------------+
    |F|R|R|R| opcode|M| Payload len |    Extended payload length    |
    |I|S|S|S|  (4)  |A|     (7)     |             (16/64)           |
    |N|V|V|V|       |S|             |   (if payload len==126/127)   |
    | |1|2|3|       |K|             |                               |
    +-+-+-+-+-------+-+-------------+ - - - - - - - - - - - - - - - +
    |     Extended payload length continued, if payload len == 127  |
    + - - - - - - - - - - - - - - - +-------------------------------+
    |                               |Masking-key, if MASK set to 1  |
    +-------------------------------+-------------------------------+
    | Masking-key (continued)       |          Payload Data         |
    +-------------------------------- - - - - - - - - - - - - - - - +
    :                     Payload Data continued ...                :
    + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
    |                     Payload Data continued ...                |
    +---------------------------------------------------------------+
"""

# Keys
LBL = 'LABEL'
LOW = 'LOW_BYTE'
HIGH = 'HIGH_BYTE'
BIT_MASK = 'BIT_MASK'
OFFSET = 'OFFSET'
LEN = 'BYTE_LENGTH'

# Format Information
FIN = {
    'LABEL': "Fin",
    'LOW_BYTE': 0,
    'HIGH_BYTE': 0,
    'BIT_MASK': 128,
    'BYTE_LENGTH': 1,
    'OFFSET': 7
}

OPCODE = {
    'LABEL': "OpCode",
    'LOW_BYTE': 0,
    'HIGH_BYTE': 0,
    'BIT_MASK': 15,
    'BYTE_LENGTH': 1,
    'OFFSET': 0
}

MASK = {
    'LABEL': "Mask",
    'LOW_BYTE': 1,
    'HIGH_BYTE': 1,
    'BIT_MASK': 128,
    'BYTE_LENGTH': 4,
    'OFFSET': 7
}

PAYLOAD_LEN = {
    'LABEL': "Payload Length",
    'LOW_BYTE': 1,
    'HIGH_BYTE': 1,
    'BIT_MASK': 127,
    'BYTE_LENGTH': 1,
    'OFFSET': 0
}

PAYLOAD_LEN_EXT_126 = {
    'LABEL': "Extended Payload Length (126)",
    'LOW_BYTE': 2,
    'HIGH_BYTE': 3,
    'BIT_MASK': 65535,
    'BYTE_LENGTH': 2,
    'OFFSET': 0
}

PAYLOAD_LEN_EXT_127 = {
    'LABEL': "Extended Payload Length (127)",
    'LOW_BYTE': 2,
    'HIGH_BYTE': 9,
    'BIT_MASK': 9223372036854775807,
    'BYTE_LENGTH': 8,
    'OFFSET': 0
}

MASK_KEY = {  # The starting bytes for the mask key depend on the payload length format and should be set dynamically.
    'LABEL': "Masking Key",
    'LOW_BYTE': None,
    'HIGH_BYTE': None,
    'BIT_MASK': 4294967295,
    'BYTE_LENGTH': 4,
    'OFFSET': 0
}

PAYLOAD = {  # The low/high bytes for the payload depend on the payload length format and should be set dynamically.
    'LABEL': "Payload",
    'LOW_BYTE': None,
    'HIGH_BYTE': None,
    'BIT_MASK': 0,
    'BYTE_LENGTH': None,
    'OFFSET': 0
}

from enum import IntEnum


class FrameType(IntEnum):
    CONTINUATION = 0
    TEXT = 1
    BINARY = 2
    CLOSE = 8
    PING = 9
    PONG = 10
