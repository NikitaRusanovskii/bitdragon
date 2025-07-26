import threading
import time
import socket

class Keeper(threading.Thread):
    """Сохраняет UDP-hole с помощью отправки отдельным потоком пустых сообщений
    (содержащих b'\x00') с периодом раз в 20 секунд.
    
    Attributes:
        sock (socket.socket) - сокет клиента, запускающего экземпляр данного класса.
        target_addr (tuple) - адрес (ip, port), на который отправляются пакеты."""
    def __init__(self, sock: socket.socket, target_addr: tuple):
        super().__init__()
        self.sock = sock
        self.target_addr = target_addr

    def run(self):
        """Переопределение метода run из threading.Thread.
        Он запускает цикл отправки сообщений."""
        while True:
            try:
                self.sock.sendto(b'\x00', self.target_addr)
                time.sleep(20)
            except Exception as ex:
                print(f'Ошибка продления соединения {ex}')
                break
