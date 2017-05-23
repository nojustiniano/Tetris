import socket
import threading
from abc import abstractmethod


class Lan:
    @abstractmethod
    def start(self, address):
        pass

    @abstractmethod
    def send_data(self, data):
        pass

    @abstractmethod
    def get_data(self):
        pass


class LanServer(Lan):
    def __init__(self):
        self.connection = None
        self.lock = threading.Lock()
        self.input_data = ""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self, address):
        self.sock.bind(address)
        self.sock.listen(5)
        d = threading.Thread(target=self.demon, name='Daemon', args=())
        d.setDaemon(True)
        d.start()

    def demon(self):
        while True:
            self.connection, client_address = self.sock.accept()
            try:
                while True:
                    self.lock.acquire()
                    data = self.connection.recv(1024)
                    if data:
                        self.input_data = data
                    else:
                        break
                    self.lock.release()
            finally:
                self.connection.close()

    def send_data(self, data):
        self.connection.sendall(str(data).encode('utf-8'))

    def get_data(self):
        return self.input_data


class LanClient(Lan):
    def __init__(self):
        self.lock = threading.Lock()
        self.input_data = ""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self, address):
        self.sock.connect(address)
        d = threading.Thread(target=self.demon, name='Daemon', args=())
        d.setDaemon(True)
        d.start()

    def demon(self):
        while True:
            self.lock.acquire()
            data = self.sock.recv(1024)
            if data:
                self.input_data = data
            else:
                break
            self.lock.release()

    def send_data(self, data):
        self.sock.sendall(str(data).encode('utf-8'))

    def get_data(self):
        return self.input_data
