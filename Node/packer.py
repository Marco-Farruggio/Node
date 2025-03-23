import struct
from typing import Union

def pack(sender_id: Union[int, str], message: str, encoding: str) -> bytes:
    """Sender ID (32Bit)"""
            
    return struct.pack("!I", sender_id) + message.encode(encoding)