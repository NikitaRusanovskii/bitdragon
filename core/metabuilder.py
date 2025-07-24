import hashlib
import os
import json


def get_hash(path: str) -> hashlib.sha512:
    h = hashlib.sha512()
    with open(path, 'rb') as hashed_file:
        while ch := hashed_file.read(8192):
            h.update(ch)
    return h


# Builder - создатель bit-файла, содержащего meta-info о раздаче.
class Builder:
    def __init__(self, addr, id):
        self.ip, self.port = addr
        self.id = id
        self.head_info = None
    
    def create_meta(self, path: str):
        
        self.head_info = {
            'file_path': path,
            'file_size': os.path.getsize(path),
            'file_hash': str(get_hash(path)),
            'peers': {},
        }
        info_str = json.dumps(self.head_info)
        info_hash = hashlib.sha512(info_str.encode()).hexdigest()
        self.head_info['head_hash'] = info_hash
        
        with open(f'{info_hash[:16]}.bit', 'w') as bit_file:
            bit_file.write(json.dumps(self.head_info))

    def update_meta(self):
        self_info = {
        'ip': self.ip,
        'port': self.port,
        'pieces': []
        }   
        self.head_info['peers'][self.id] = self_info