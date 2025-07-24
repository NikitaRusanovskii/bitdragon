import socket
import struct
import time

class Downloader:
    def __init__(self, sock: socket.socket, peer_ip: str, peer_port: int):
        self.sock = sock
        self.peer_ip = peer_ip
        self.peer_port = peer_port

    def request_download(self, part):
        try:
            self.header = struct.pack('>II', part, 256)
            self.sock.sendto(self.header, (self.peer_ip, self.peer_port))
        except Exception as ex:
            print(f'Ошибка при отправке запроса на пакет: {ex}')

    def receive_part(self, parts: dict):
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
    def __init__(self, path_to_write: str):
        self.path_to_write = path_to_write

    def write_in_file(self, parts):
        with open(self.path_to_write, 'wb') as file:
            for i in sorted(parts):
                try:
                    file.write(parts[i])
                except:
                    break