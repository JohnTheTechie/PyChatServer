import socket
from enum import Enum


class SockAddressContainer:
    def __init__(self, address=None, port=None):
        self.address = address
        self.port = port

    def get_address(self):
        return self.address

    def get_port(self):
        return self.port


class SocketType(Enum):
    SOCKET_CLIENT = 0x01
    SOCKET_SERVER = 0x02


class SocketConnection:
    def __init__(self, address_con: SockAddressContainer, s_type:SocketType):
        self.s_type = s_type
        self.address_container = address_con
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection = None


class ServerSocket(SocketConnection):
    def __init__(self, address_con: SockAddressContainer, s_type:SocketType):
        SocketConnection.__init__(self, address_con, s_type)
        self.socket.bind((self.address_container.address, self.address_container.port))



