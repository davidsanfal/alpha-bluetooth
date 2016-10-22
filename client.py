import threading
from collections import namedtuple
from exceptions import AlphaException

Message = namedtuple('Message', ['read', 'write'])


class ThreadedClient(object):
    def __init__(self):
        self.port = 1
        self.msg = Message([], [])
        self.bd_addr = self.discover()
        self.sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        self._close = False

    @staticmethod
    def discover():
        print("discovering ...")
        nearby_devices = bluetooth.discover_devices(lookup_names=True)
        print("found %d devices" % len(nearby_devices))

        for addr, name in nearby_devices:
            if name == "ALPHA 1S":
                return addr
        raise AlphaException()

    def connect(self):
        self.sock.connect((self.bd_addr, self.port))
        self.read_thread = threading.Thread(target = self.listen).start()
        self.write_thread = threading.Thread(target = self.write).start()

    def write(self):
        while not self._close:
            if self.msg.write:
                try:
                    self.sock.send(self.msg.write.pop())
                except Exception as e:
                    print(e)
                    self.close()

    def listen(self):
        while not self._close:
            try:
                data = self.sock.recv(1024)
                if data:
                    self.msg.read.append(data)
            except Exception as e:
                print(e)
                self.close()

    def close(self):
        self._close = True
        self.read_thread.join()
        self.write_thread.join()
        self.sock.close()
