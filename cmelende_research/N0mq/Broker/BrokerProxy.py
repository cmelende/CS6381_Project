import zmq


class BrokerProxy:
    def __init__(self, host_address: str, receive_port: str, sending_port: str):
        self._isRunning = True
        self._context = zmq.Context.instance()
        self._receiving_socket = self._context.socket(zmq.XSUB)
        self._receiving_socket.bind("tcp://{}:{}".format(host_address, receive_port))

        self._sending_socket = self._context.socket(zmq.XPUB)
        self._sending_socket.bind("tcp://{}:{}".format(host_address, sending_port))
        self._proxy: zmq.proxy = None

    def run(self):
        try:
            self._proxy = zmq.proxy(self._sending_socket, self._receiving_socket)
        except KeyboardInterrupt:
            self.close()

    def close(self) -> None:
        self._receiving_socket.close()
        self._sending_socket.close()
        self._context.term()
