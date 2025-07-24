import threading
import time

class Keeper(threading.Thread):
    def __init__(self, sock, target_addr):
        super().__init__()
        self.sock = sock
        self.target_addr = target_addr

    def run(self):
        while True:
            try:
                self.sock.sendto(b'\x00', self.target_addr)
                time.sleep(20)
            except Exception as ex:
                print(f'Ошибка продления соединения {ex}')
                break
