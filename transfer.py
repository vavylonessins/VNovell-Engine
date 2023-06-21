from thread import *
import socket

class DataSender:
    def __init__(self, port=9090, host=''):
        print(f"[LOG] [{__file__}] initializing data sender at [tcp://{host}:{port}/]...")
        self.port = port
        self.host = host
        print(f"[LOG] [{__file__}]    opening socket")
        self.socket = socket.socket()
        print(f"[LOG] [{__file__}]    connecting")
        self.socket.connect((self.host, self.port))
        print(f"[LOG] [{__file__}] Done")
    
    def send(self, data: object):
        print(f"[LOG] [{__file__}] Sending data to [tcp://{self.host}:{self.port}/]...")
        self.socket.sendall(repr(data).encode('utf-8'))
        print(f"[LOG] [{__file__}] Done")


class DataReceiver:
    def __init__(self, port=9090, host=''):
        print(f"[LOG] [{__file__}] initializing data receiver at [tcp://{host}:{port}/]...")
        self.port = port
        self.host = host
        print(f"[LOG] [{__file__}]    opening socket")
        self.socket = socket.socket()
        print(f"[LOG] [{__file__}]    binding socket")
        self.socket.bind((self.host, self.port))
        self.data = None
        print(f"[LOG] [{__file__}] Done")
    
    @thread
    def listen(self, queue=255):
        print(f"[LOG] [{__file__}] listening socket...")
        self.socket.listen(queue)
        self.conn, self.addr = self.socket.accept()
        self.run = True

        while self.run:
            try:
                self.data = eval(self.conn.recv(1024).decode('utf-8'))
                self.conn.send(b'\x01')
            except:
                self.conn.send(b'\x00')
        print(f"[LOG] [{__file__}] Done")

    def stop(self):
        print(f"[LOG] [{__file__}] stopping listening queue...")
        assert self.run
        self.run = False
        print(f"[LOG] [{__file__}] Done")
    
    def receive(self):
        return self.data
