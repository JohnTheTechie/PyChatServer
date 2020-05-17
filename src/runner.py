from src import thread_handlers
from src import sockets
import logging


if __name__ == '__main__':

    logging.basicConfig(filename='example.log', level=logging.DEBUG)

    request_queue = thread_handlers.ClientQueue().get_queue()
    logging.debug(f"queue created | {request_queue}")

    dispatcher_thread = thread_handlers.Dispatcher(request_queue)
    logging.debug(f"queue is operational | {dispatcher_thread.queue}")
    dispatcher_thread.start()

    server_socket = sockets.ServerSocket(sockets.SockAddressContainer(), sockets.SocketType.SOCKET_SERVER, request_queue)
    server_socket.loop_and_look_for_connection_requests()

    dispatcher_thread.join()
