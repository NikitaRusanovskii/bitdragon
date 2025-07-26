import socket
import threading
from core import Keeper
from core.downloader import *
from core.uploader import *

class Connector(threading.Thread):
    """Коннектор служит связующим звеном между двумя пирами.
    Наследуется от threading.Thread. Один клиент может запускать
    несколько сотен коннекторов. Каждый коннектор может выступать
    либо Downloader'ом, либо Uploader'ом.
    
    Attributes:
        name (str) - имя клиента.
        my_ip (str) - ip-адрес клиента.
        my_port (int) - port клиента.
        peer_ip (str) - ip-адрес клиента, с которым соединяемся.
        peer_port (int) - port клиента, с которым соединяемся.
        sock (socket.socket) - сокет текущего клиента."""
    def __init__(self, name: str, my_addr: tuple, peer_addr: tuple):
        super().__init__()
        self.name = name
        self.my_ip = my_addr[0]
        self.my_port = int(my_addr[1])
        self.peer_ip = peer_addr[0]
        self.peer_port = int(peer_addr[1])
        self.sock = None
        #self.header = None
    def punch(self):
        """Выполняет udp hole punch для установления соединения между клиентами.
        Запускает Keeper, который сохраняет это соединение."""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('', self.my_port))

        #kp = Keeper(self.sock, (self.peer_ip, self.peer_port))
        #self.sock.sendto(b'\x00', (self.peer_ip, self.peer_port))
        #kp.start()

    def work_loop(self):
        """Жизненный цикл коннектора. Позволяет выбрать режим работы (загрузка или отправка)."""
        mode = input('> select upload or download: ')
        if mode == 'upload':
            u = Uploader('tests\\test_file.txt', 256, self.peer_ip, self.peer_port, self.sock)
            u.work_loop()
        else:
            parts_count = 4096
            parts = {}
            d = Downloader(self.sock, self.peer_ip, self.peer_port)
            w = Writer('tests\\test_download.txt')
            for part in range(parts_count):
                d.request_download(part)
                d.receive_part(parts)
            w.write_in_file(parts)
            
                


    def run(self):
        """Переопределение метода run из threading.Thread"""
        self.punch()
        self.work_loop()

class Client:
    """Устанавливает соединение со всеми возможными компьютерами.
    
    Attributes:
        addr (tuple) - кортеж, содержащий айпи и порт клиента.
        name (str) - имя клиента
        peers (dict) - список пиров, с которыми нужно соединиться."""
    def __init__(self, addr: tuple, name: str, peers: dict):
        self.addr = addr
        self.name = name
        self.peers = peers

    def start(self):
        """Запускает и отключает коннекторы."""
        connectors = [Connector(self.name, self.addr, self.peers[id]) for id in self.peers]
        for c in connectors:
            c.start()

        for c in connectors:
            c.join()