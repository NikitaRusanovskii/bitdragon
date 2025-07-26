import socket
import struct

class Downloader:
    """Выполняет загрузку файла по частям в словарь.
        
    Attributes:
        sock (socket.socket) - сокет клиента.
        peer_ip (str) - ip пира, к которому подключается клиент.
        peer_port (int) - port пира, к которому подключается клиент"""
    def __init__(self, sock: socket.socket, peer_ip: str, peer_port: int):
        self.sock = sock
        self.peer_ip = peer_ip
        self.peer_port = peer_port

    def request_download(self, part: int):
        """Отправляет запрос на загрузку определенного фрагмента файла по индексу.
        Каждый фрагмент - 256 бит.
        
        Args:
            part (int) - номер части файла."""
        try:
            self.header = struct.pack('>II', part, 256)
            self.sock.sendto(self.header, (self.peer_ip, self.peer_port))
        except Exception as ex:
            print(f'Ошибка при отправке запроса на пакет: {ex}')

    def receive_part(self, parts: dict):
        """Получает часть файла и записывает в словарь parts, содержащий
        пары (номер части - часть).
        Args:
            parts (dict) - словарь, содержащий """
        try:
            data, addr = self.sock.recvfrom(264)
            if len(data) == 264:
                part, lenght = struct.unpack('>II', data[:8])
                chunk = data[8:]
                parts[part] = chunk
                print(f'Получен чанк {part}')
            else:
                print(data.decode())
        except Exception as ex:
            print(f'Ошибка при получении пакета: {ex}')

class Writer:
    """Записывает полученные части в файл в нужном порядке.
    
    Attributes:
        path_to_write (str) - абсолютный путь к файлу, куда записываются части файла."""
    def __init__(self, path_to_write: str):
        self.path_to_write = path_to_write

    def write_in_file(self, parts: dict):
        """Записывающая в файл функция.
        
        Args:
            parts (dict) - словарь с частями файлов. (номер, часть файла)"""
        with open(self.path_to_write, 'wb') as file:
            for i in sorted(parts):
                try:
                    file.write(parts[i])
                except:
                    break