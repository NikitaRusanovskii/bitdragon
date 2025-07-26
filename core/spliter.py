def split(path: str, chunk_size: int) -> dict:
    """Разбивает файл на части по заданному размеру.
    
    Args:
        path (str) - абсолютный путь к разбиваемому файлу.
        chunk_size (int) - размер части, на которые разбиваем.
    
    Returns:
        Словарь, содержащий пару [номер: часть файла].
    """
    chunk_id = 0
    splited_file = {}
    try:
        with open(path, 'rb') as file:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                splited_file[chunk_id] = chunk
                chunk_id+=1
    except FileNotFoundError as ex:
        print(f'Ошибка. Файл не найден: {ex}')
    return splited_file
