########################################################################################################################
# author            :   Janakiraman Jothimony
# created date      :   18-05-2019
# modified date     :   19-05-2019
# version           :   1.2
# description       :   classes defining the socket behaviours and related components
########################################################################################################################

import socket
from enum import Enum
import queue
import logging


class SockAddressContainer:
    """
    address capsule for socket address
    """
    def __init__(self, address="localhost", port=42424):
        self.address = address
        self.port = port

    def get_address(self):
        return self.address

    def get_port(self):
        return self.port


class SocketType(Enum):
    """
    enumeration class for types of sockets to be used
    """
    SOCKET_CLIENT = 0x01
    SOCKET_SERVER = 0x02


class SocketConnection:
    """
    Base class for sockets
    """
    def __init__(self, address_con: SockAddressContainer, s_type: SocketType):
        self.s_type = s_type
        self.address_container = address_con
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection = None


class ServerSocket(SocketConnection):
    """
    socket tuned for listening to connect requests
    """
    def __init__(self, address_con: SockAddressContainer, s_type: SocketType, socket_queue: queue.Queue):
        logging.debug(f"{self.__class__} | ServerSocket init started")
        # init the super class
        SocketConnection.__init__(self, address_con, s_type)

        # bind to the project socket address and start listening
        self.socket.bind((self.address_container.address, self.address_container.port))
        # TODO: implement and add reference class for providing the data
        self.socket.listen(5)

        self.socket_queue = socket_queue

        logging.debug(f"{self.__class__} | queue obtained: {self.socket_queue}")
        logging.debug(f"{self.__class__} | server socket created | address: {self.address_container.address} |"
                      f" port: {self.address_container.port}")

    def loop_and_look_for_connection_requests(self):
        """
        the function initiates infinite loop and listens for the connection request
        On accepting the socket, the same is pushed to the queue for consumption by the dispatcher
        """

        while True:
            logging.debug(f"{self.__class__} | looking for connection requests")
            (conn_socket, address) = self.socket.accept()
            logging.debug(f"{self.__class__} | connection request received | "
                          f"address: {address} | new_socket: {conn_socket}")
            self.socket_queue.put(conn_socket)
