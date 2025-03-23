import socket

class ClientNode(socket.socket):
    def __init__(self, address_family, protocol, server_ip, port, encoding: str = "utf-8") -> None:
        super().__init__(address_family, protocol)

        self.SERVER_IP = server_ip
        self.PORT = port
        self.encoding = encoding

        self.connect((self.SERVER_IP, self.PORT))

    def transmit(self, msg: str) -> None:
        self.sendall(msg.encode(self.encoding))