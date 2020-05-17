from threading import Thread
from queue import Queue
import socket
import logging


class ClientQueue:
    """
    class for controlling the creation of queue
    """

    # container for singleton object
    __singleton = None

    def __init__(self):
        """
        initialize the queue object

        Only creates a queue and encapsulates it
        """
        logging.debug(f"{self.__class__} | created")
        self.__q = Queue()

    def __new__(cls, *args, **kwargs):
        if cls.__singleton is None:
            cls.__singleton = object.__new__(cls)
        return cls.__singleton

    def get_queue(self):
        """
        returns the queue
        :return: queue
        """
        logging.debug(f"{self.__class__} | queue obtained")
        return self.__q


class Dispatcher(Thread):
    """
    thread to check the queue and dispatch the tasks to different threads
    """

    __singleton = None

    def __init__(self, queue, *args, **kwargs):
        self.queue: Queue = queue
        Thread.__init__(self, *args, **kwargs)

    def __new__(cls, *args, **kwargs):
        if cls.__singleton is None:
            cls.__singleton = object.__new__(cls)
        return cls.__singleton

    def run(self) -> None:
        logging.debug(f"{self.__class__} | Dispatcher started and running with queue {self.queue}")
        while True:
            item = self.queue.get()
            print(f"{self.__class__} | Dispatcher received socket: {item}")
            self.pass_on_the_message(item)

    def pass_on_the_message(self, item):
        """
        when the dispatcher retrieves a socket from the queue, it evaluates the content,
        creates a relevant thread to process the socket
        """
        worker: Thread = WorkerThread(item)
        worker.start()
        logging.debug(f"{self.__class__} | Dispatcher passed on the received socket: {item}")


class WorkerThread(Thread):
    """
    simple class to receive and read the sockets received

    this class is to be only used for testing purposes
    """
    def __init__(self, socket_connection, *args, **kwargs):
        self._socket: socket.socket = socket_connection
        logging.debug(f"{self.__class__} | worker thread created with socket {self._socket}")
        Thread.__init__(self, *args, **kwargs)

    def run(self) -> None:
        logging.debug(f"{self.__class__} | worker thread started running with socket {self._socket}")
        buffer = self._socket.recv(1024).decode()
        print(buffer)


