import socket
import threading
from core import Keeper
from core.downloader import *
from core.uploader import *

class Connector(threading.Thread):
    def __init__(self, name: str, my_addr: tuple, peer_addr: tuple):
        super().__init__()
        self.name = name
        self.my_ip = my_addr[0]
        self.my_port = int(my_addr[1])
        self.peer_ip = peer_addr[0]
        self.peer_port = int(peer_addr[1])
        self.sock = None
        self.header = None
    def punch(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('', self.my_port))

        kp = Keeper(self.sock, (self.peer_ip, self.peer_port))
        self.sock.sendto(b'Hello from peer', (self.peer_ip, self.peer_port))
        kp.start()

    def work_loop(self):
        mode = input('> select upload or download: ')
        if mode == 'upload':
            u = Uploader('test_file.txt', 256, self.peer_ip, self.peer_port, self.sock)
            u.work_loop()
        else:
            parts_count = 4096
            parts = {}
            d = Downloader(self.sock, self.peer_ip, self.peer_port)
            w = Writer('test_download.txt')
            for part in range(parts_count):
                d.request_download(part)
                d.receive_part(parts)
            w.write_in_file(parts)
            
                


    def run(self):
        self.punch()
        self.work_loop()

class Client:
    def __init__(self, addr: tuple, name: str, peers: dict):
        self.addr = addr
        self.name = name
        self.peers = peers

    def start(self):
        connectors = [Connector(self.name, self.addr, self.peers[id]) for id in self.peers]
        for c in connectors:
            c.start()

        for c in connectors:
            c.join()