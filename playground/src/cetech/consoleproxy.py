import msgpack
from nanomsg import Socket, REQ


class ConsoleProxy(object):
    def __init__(self, url):
        super(ConsoleProxy, self).__init__()
        self.url = url
        self.socket = Socket(REQ)

    def connect(self):
        self.socket.connect(self.url)

    # TODO: dangerous, block
    def send_command_norcv(self, cmd_name, echo=False, **kwargs):
        command = {
            "name": cmd_name,
            "args": kwargs
        }

        dump = msgpack.packb(command)

        if echo:
            print('send: ', command)

        self.socket.send(dump)

    def send_command(self, cmd_name, echo=False,**kwargs):
        self.send_command_norcv(cmd_name=cmd_name, echo=echo, **kwargs)
        recv = self.socket.recv()

        unpack_msg = msgpack.unpackb(recv, encoding='utf-8')

        if echo:
            print('recv: ', recv)
            print(unpack_msg)

    def disconnect(self):
        self.socket.close()