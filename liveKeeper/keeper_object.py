import threading
import time

class Keeper:
    def __init__(self, sock, target_addr):
        self.sock = sock
        self.target_addr = target_addr

    def keep_alive(self):
        while True:
            try:
                self.sock.sendto(b'\x00', self.target_addr)
                time.sleep(20)
            except Exception as ex:
                print(f'! keep alive error\n{ex}')
                break

    def start(self):
        threading.Thread(target=self.keep_alive, daemon=True).start()