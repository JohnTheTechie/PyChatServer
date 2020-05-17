import thread_handlers
import sockets


if __name__ == '__main__':
    request_queue = thread_handlers.ClientQueue().get_queue()
    print(f"queue created | {request_queue}")

    dispatcher_thread = thread_handlers.Dispatcher(request_queue)
    print(f"queue is operational | {dispatcher_thread.queue}")
    dispatcher_thread.start()

    server_socket = sockets.ServerSocket(sockets.SockAddressContainer(), sockets.SocketType.SOCKET_SERVER, request_queue)
    server_socket.loop_and_look_for_connection_requests()

    dispatcher_thread.join()
