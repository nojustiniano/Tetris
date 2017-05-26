import socket
import threading
import time
from abc import abstractmethod


class Lan:
    def __init__(self):
        self.connection = None
        self.lock = threading.Lock()
        self.input_data = ""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data_to_send = list()

    def start(self, address):
        self.connect(address)
        self.start_receiver_daemon()
        self.start_sender_daemon()

    @abstractmethod
    def connect(self, address):
        pass

    def receive_data(self):
        self.lock.acquire()
        file = self.connection.makefile()
        char = ''
        str_length = ''

        # read the length of data you going to receive
        while char is not ')':
            char = file.read(1)
            str_length += char

        self.input_data = file.read(eval(str_length))
        self.lock.release()

    def send_data(self, data):
        self.data_to_send.append(data)

    def get_data(self):
        return self.input_data

    def sender_daemon(self):
        while True:
            if len(self.data_to_send) > 0:
                try:
                    msg = str(self.data_to_send[0]).replace(' ', '')
                    # Append message length
                    msg = '(' + str(len(msg)) + ')' + msg
                    self.connection.sendall(msg.encode('utf-8'))
                    del self.data_to_send[0]
                except Exception as e:
                    print("Error sending data: " + str(e))
            time.sleep(0.1)

    def start_sender_daemon(self):
        t1 = threading.Thread(target=self.sender_daemon, name='sender_daemon', args=())
        t1.setDaemon(True)
        t1.start()

    def receiver_daemon(self):
        while True:
            self.receive_data()
            time.sleep(0.1)

    def start_receiver_daemon(self):
        t2 = threading.Thread(target=self.receiver_daemon, name='receiver_daemon', args=())
        t2.setDaemon(True)
        t2.start()


class LanServer(Lan):
    def connect(self, address):
        self.sock.bind(address)
        self.sock.listen(5)
        while self.connection is None:
            self.connection, client_address = self.sock.accept()


class LanClient(Lan):
    def connect(self, address):
        self.sock.connect(address)
        self.connection = self.sock
