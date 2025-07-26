import hashlib
import os
import json
from core.spliter import split


def get_hash(path: str) -> str:
    """Вычисляет SHA-512 хеш файла.
    Файл читается блоками по 8192 байта для лучшей производительности.
    
    Args: 
        path: абсолютный путь к файлу.
    
    Returns:
        Шестнадцатиричная строка с хешем файла. 
    """
    h = hashlib.sha512()
    with open(path, 'rb') as hashed_file:
        while ch := hashed_file.read(8192):
            h.update(ch)
    return h.hexdigest()

def write_meta(info: dict) -> None:
    """Генерирует мета-файл раздачи (.bit) в формате json
    Автоматически добавляет хеш мета-файла перед записью.
    
    Args:
        info: словарь с мета-информацией. (Будет изменён,
        к нему добавится head-hash (хеш мета-файла))"""
    info_str = json.dumps(info)
    info_hash = hashlib.sha512(info_str.encode()).hexdigest()
    info['head_hash'] = info_hash
        
    with open(f'{os.path.basename(info['file_path']).split('.')[0]}.bit', 'w') as bit_file:
        bit_file.write(json.dumps(info))



# Builder - создатель bit-файла, содержащего meta-info о раздаче.
class Builder:
    """Генерирует и управляет мета-информацией о раздаче в формате bit-файлов.
    
    Attributes:
        ip (str) - IP-адрес текущего пира.
        port (str) - порт текущего пира.
        id (int) - уникальный идентификатор текущего пира.
        head_info - словарь, содержащий мета-информацию о файле.
    """
    def __init__(self, addr: tuple, id: int):
        self.ip, self.port = addr
        self.id = id
        self.head_info = None
    
    def create(self, path: str, chunk_size: int):
        """Создаёт мета-файл с информацией о раздаче.
        
        Args:
            path: абсолютный путь до файла раздачи
            chunk_size: размер одного чанка файла
        """
        self.head_info = {
            'file_path': path,
            'file_size': os.path.getsize(path),
            'file_hash': str(get_hash(path)),
            'chunk_size': chunk_size,
            'chunks' : len(split(path, chunk_size)),
            'peers': {},
        }
        write_meta(self.head_info)

    def update(self):
        """Обновляет информацию в мета-файле, добавляя
        свой адрес и идентификатор в поле peers.
        """
        self_info = {
        'ip': self.ip,
        'port': self.port,
        'pieces': []
        }   
        self.head_info['peers'][self.id] = self_info
        write_meta(self.head_info)


    def upload(self):
        """Выгружает обновлённый или созданный мета-файл на трекер"""
        pass