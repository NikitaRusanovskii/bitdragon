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
    def __init__(self):
        pass
    
    def create_meta_file(self, path: str):
        
        head_info = {
            'file_path': path,
            'file_size': os.path.getsize(path),
            'file_hash': str(get_hash(path)),
            'peers': [],
        }
        info_str = json.dumps(head_info)
        info_hash = hashlib.sha512(info_str.encode()).hexdigest()
        head_info['head_hash'] = info_hash
        
        with open(f'{info_hash[:16]}.bit', 'w') as bit_file:
            bit_file.write(json.dumps(head_info))