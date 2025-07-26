import json

class Reader:
    """Читает мета-файл раздачи (.bit)
        
    Attributes:
        path (str) - абсолютный путь к файлу раздачи."""
    def __init__(self, path: str):
        self.path = path

    def read(self) -> tuple:
        """Читает мета-файл.
            
        Returns:
            Кортеж, содержащий размер чанка и количество чанков в файле"""
        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return (data['chunk_size'], data['chunks'])
        except Exception as ex:
            print(f'Ошибка при чтении файла {ex}')

    def download(self):
        """Скачивает с трекера мета-файл раздачи,
        если он был обновлён."""
        pass