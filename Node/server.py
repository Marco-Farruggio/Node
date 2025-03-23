import socket
import struct

class ServerNode(socket.socket):
    def __init__(self, address_family, protocol, listening_addr, port, encoding: str = "utf-8") -> None:
        super().__init__(address_family, protocol)
        
        self.HOST = listening_addr
        self.PORT = port
        self.encoding = encoding

        self.bind((self.HOST, self.PORT))

    def recvall(self, conn) -> None:
        data = conn.recv(4)
        if not data:
            return None, None

        sender_id = struct.unpack("!I", data)[0]
        message = b""

        while True:
            chunk = conn.recv(1024)

            if not chunk:
                break

            message += chunk

        return sender_id, message.decode(self.encoding)