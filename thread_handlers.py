from threading import Thread
from queue import Queue


class ClientQueue:
    """
    class for controlling the creation of queue
    """

    # container for sigleton object
    __singleton = None

    def __init__(self):
        """
        initialize the queue object

        Only creates a queue and encapsulates it
        """
        self.__q = Queue()

    def __new__(cls, *args, **kwargs):
        if cls.__singleton is None:
            cls.__singleton = object.__new__(cls)
        return cls.__singleton

    def get_queue(self):
        """
        returns the queue
        :return:
        """
        return self.__q


class SocketListenerThreads(Thread):
    def __init__(self, queue, ):
        Thread.__init__(self)

