import socket
import struct
import time


class Uploader:
    def __init__(self, path: str, chunk_size: int, peer_ip: str, peer_port: int, sock: socket.socket):
        self.path = path
        self.chunk_size = chunk_size
        self.splited_file = {}
        self.peer_ip = peer_ip
        self.peer_port = peer_port
        self.sock = sock

    def split_file(self, nec_chunks: list):
        chunk_id = 0
        try:
            with open(self.path, 'rb') as file:
                while True:
                    chunk = file.read(self.chunk_size)
                    if not chunk:
                        break
                    if chunk_id in nec_chunks:
                        self.splited_file[chunk_id] = chunk
                    chunk_id += 1
        except FileNotFoundError as ex:
            print(f'Ошибка. Файл не найден: {ex}')
        missing = set(nec_chunks) - set(self.splited_file)
        if missing:
            print(f'Ошибка при запросе файла, чанки {missing} отсутствуют')
        
    def wait_request(self):
        while True:
            try:
                data, addr = self.sock.recvfrom(8)
                if len(data) == 8:
                    part, ln = struct.unpack('>II', data)
                    return (part, ln)
            except Exception as ex:
                print(f'Ошибка в ожидании запроса: {ex}')
            
    def upload_file(self, part: int):
        try:
            for ch in list(self.splited_file): # копия ключей
                chunk = self.splited_file.pop(ch)
                header =  struct.pack('>II', ch, len(chunk)) # '>II' - формат кодирования.
                # > - числа будут закодированы в сетевом порядке байт
                # I - беззнаковый целочисленный тип
                self.sock.sendto(header + chunk, (self.peer_ip, self.peer_port))
        except Exception as ex:
            print(f'Ошибка. Соединение прервано: {ex}')

    def work_loop(self):
        while True:
            try:
                part, length = self.wait_request()
                self.split_file([part])
                self.upload_file(part)
            except Exception as ex:
                print(f'Ошибка в работе Uploader: {ex}')