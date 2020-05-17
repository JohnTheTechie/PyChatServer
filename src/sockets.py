import socket
from enum import Enum
import queue
import threading
import thread_handlers


class SockAddressContainer:
    def __init__(self, address="localhost", port=42424):
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
    def __init__(self, address_con: SockAddressContainer, s_type: SocketType):
        self.s_type = s_type
        self.address_container = address_con
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection = None


class ServerSocket(SocketConnection):
    def __init__(self, address_con: SockAddressContainer, s_type: SocketType, socket_queue: queue.Queue):
        SocketConnection.__init__(self, address_con, s_type)
        self.socket.bind((self.address_container.address, self.address_container.port))
        self.socket.listen(5)
        self.socket_queue = socket_queue
        print(f"{self.__class__} | queue obtained: {self.socket_queue}")
        print(f"{self.__class__} | server socket created | address: {self.address_container.address} | port: {self.address_container.port}")

    def start_listening(self):
        pass

    def loop_and_look_for_connection_requests(self):
        while True:
            (conn_socket, address) = self.socket.accept()
            print(f"{self.__class__} | connection request received | address: {address} | new_socket: {conn_socket}")
            self.socket_queue.put(conn_socket)


