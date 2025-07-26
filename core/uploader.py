import socket
import struct
from core.spliter import split


class Uploader:
    """Ожидает запрос на необходимый чанк файла. После получения запроса отправляет чанк
    с соответствующим номером.
    
    Attributes:
        path (str) - абсолютный путь к файлу, который раздаётся.
        chunk_size (int) - размер отправляемого чанка.
        peer_ip (str) - айпи пира, которому отправляем данные.
        peer_port (int) - порт пира, которому отправляем данные.
        sock (socket.socket) - сокет клиента, который управляет объектом данного класса."""
    def __init__(self, path: str, chunk_size: int, peer_ip: str, peer_port: int, sock: socket.socket):
        self.path = path
        self.chunk_size = chunk_size
        self.peer_ip = peer_ip
        self.peer_port = peer_port
        self.sock = sock
        
    def wait_request(self):
        """Ожидает запрос на чанк в виде (номер, длина).
        
        Returns:
            кортеж, состоящий из номера чанка и его длины.
        """
        while True:
            try:
                data, addr = self.sock.recvfrom(8)
                if len(data) == 8:
                    part, ln = struct.unpack('>II', data)
                    return (part, ln)
            except Exception as ex:
                print(f'Ошибка в ожидании запроса: {ex}')
            
    def upload_file(self, part: int, splited_file: dict):
        """Загружает файл пиру.
        
        Args:
            part (int) - часть, которую отправляем.
            splited_file (dict) - словарь, содержащий все части файла с их номерами."""
        try:
            for ch in list(splited_file): # копия ключей
                if ch == part:
                    chunk = splited_file.pop(ch)
                    header =  struct.pack('>II', ch, len(chunk)) # '>II' - формат кодирования.
                    # > - числа будут закодированы в сетевом порядке байт
                    # I - беззнаковый целочисленный тип
                    self.sock.sendto(header + chunk, (self.peer_ip, self.peer_port))
        except Exception as ex:
            print(f'Ошибка. Соединение прервано: {ex}')

    def work_loop(self):
        """Выполняет рабочий цикл: разбивает файл на части.
        Запускает ожидание запроса на часть файла.
        Отправляет часть файла."""
        sf = split(self.path, self.chunk_size)
        while True:
            try:
                part, length = self.wait_request()
                self.upload_file(part, sf)
            except Exception as ex:
                print(f'Ошибка в работе Uploader: {ex}')