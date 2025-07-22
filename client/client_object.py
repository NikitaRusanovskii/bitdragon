import socket
import threading
from liveKeeper import Keeper

class Client:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def punch(self, friend_ip, friend_port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', self.port))

        kp = Keeper(sock, (friend_ip, int(friend_port)))

        sock.sendto(b'Hello from peer', (friend_ip, int(friend_port)))
        kp.start()

        threading.Thread(target=self.receiver_loop, daemon=True).start()

        while True:
            msg = str(input('type your msg > '))
            if msg == 'exit':
                break
            sock.sendto(msg.encode(), (friend_ip, int(friend_port)))


    def receiver_loop(self):
        while True:
            try:
                data, addr = self.sock.recvfrom(1024)
                print(f"[RECV]:\n{data.decode()}\nfrom\n{addr}")
            except Exception as ex:
                print(f'!Error:\n{ex}')
                break