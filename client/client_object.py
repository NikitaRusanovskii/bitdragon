import socket
import threading
from liveKeeper import Keeper

class Client:
    def __init__(self, ip, port, name):
        self.ip = ip
        self.port = port
        self.name = name
        self.sock = None

    def punch(self, friend_ip, friend_port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('', self.port))

        kp = Keeper(self.sock, (friend_ip, int(friend_port)))

        self.sock.sendto(b'Hello from peer', (friend_ip, int(friend_port)))
        kp.start()

        threading.Thread(target=self.receiver_loop, daemon=True).start()

        while True:
            msg = str(input('type your msg > '))
            if msg == 'exit':
                break
            self.sock.sendto(msg.encode(), (friend_ip, int(friend_port)))


    def receiver_loop(self):
        while True:
            try:
                data, addr = self.sock.recvfrom(1024)
                dd = data.decode()
                if dd != str(addr[1]) and dd.rstrip() != '':
                    print(f"{self.name}: \n{data.decode()}\n")
            except Exception as ex:
                print(f'!Error:\n{ex}')
                break