from fastapi import FastAPI, HTTPException, UploadFile, File # Depends используем для внедрения зависимостей
from fastapi.responses import FileResponse
from sqlmodel import select
import os
import shutil
import logging

from models import *
from db_config import *

UPLOAD_DIR = "meta_files"
NOT_FOUND = "Meta-file not found."

app = FastAPI(lifespan=lifespan)
logger = logging.getLogger(__name__)


@app.get('/meta_files/{file_name}/peers')
def get_peers(file_name: str, session: SessionDep) -> list:
    """Возвращает все пиры, зарегистрированные на раздаче file_name.
    
    note: Выполняет select-запрос к DHT, находит поле, для которого
    верно meta_file == file_name. Возвращает его peers.
    
    Args:
        file_name (str) - имя мета-файла.
        session (SessionDep) - объект взаимодействия с базой данных.
    Returns:
        list[str]"""
    
    results = session.exec(
        select(DHT).where(DHT.meta_file==file_name)
    ).all()
    if not results:
        logger.info(f'Error in func get_peers\nstatus_code: 404, detail: {NOT_FOUND}')
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    peers = [r.peers for r in results]
    logger.info(f'Func get_peers: successful, result:\n{peers}')
    return peers

@app.get('/meta_files')
def get_meta_files(session: SessionDep) -> list:
    """Возвращает все мета-файлы из dht.
    
    Args:
        session (SessionDep): объект взаимодействия с базой данных.
    Returns:
        list[str]"""
    
    results =  session.exec(select(DHT)).all()
    if not results:
        logger.info(f'Error in func get_meta_files\nstatus_code: 404, detail: {NOT_FOUND}')
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    meta_files = [r.meta_file for r in results]
    logger.info(f'Func get_peers: successful, result:\n{meta_files}')
    return meta_files

@app.delete('/meta_files/{file_name}')
def delete_meta_file(file_name: str, session: SessionDep):
    """Удаляет запись из DHT, у которой поле meta_file содержит file_name.
    
    Args:
        file_name (str): Имя мета-файла.
        session (SessionDep): объект взаимодействия с базой данных.
    Returns:
        dict: подтверждение успешности операции"""
    file = session.exec(select(DHT).where(DHT.meta_file == file_name)).first()
    if not file:
        logger.info(f'Error in func delete_meta_file\nstatus_code: 404, detail: {NOT_FOUND}')
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    session.delete(file)
    session.commit()
    logger.info('Func delete_meta_file: successful')
    return {'successful' : True}

@app.post('/register')
def create_distribution(new_dist: DistributionModel, session: SessionDep):
    """Добавляет новую запись о раздаче в таблицу DHT.
    
    Args:
        new_dist (DistributionModel): вспомогательная модель для создания записи о новой раздаче.
        session (SessionDep): объект взаимодействия с базой данных.
    Returns:
        dict: подтверждение успешности операции"""
    new_entry = DHT(meta_file=new_dist.meta_file, peers=new_dist.peers)
    session.add(new_entry)
    session.commit()
    session.refresh(new_entry)
    res = {
        'successful': True,
        'id': new_entry.id,
        'meta_file': new_entry.meta_file,
        'peers': new_entry.peers
    }
    logger.info(f'Func create_distribution: successful, result:\n{res}')
    return res

@app.patch('/meta_files/{file_name}')
def update_DHT(file_name: str, dist_upd: DistributionUpdate, session: SessionDep):
    """Обновляет запись file_name в таблице DHT.
    
    Args:
        file_name (str): имя мета-файла.
        dist_upd (DistributionUpdate): вспомогательная модель для обновления информации в таблице.
        session (SessionDep): объект взаимодействия с базой данных.
    Returns:
        dict: подтверждение успешности операции."""
    
    dist = session.exec(select(DHT).where(DHT.meta_file==file_name)).first()
    if not dist:
        raise HTTPException(status_code=404, detail=NOT_FOUND)
    if dist_upd.peers != None:
        dist.peers = dist_upd.peers
    session.add(dist)
    session.commit()
    session.refresh(dist)

    res = {
        'successful': True,
        'meta_file': dist.meta_file,
        'peers': dist.peers
    }    
    logger.info(f'Func update_DHT: successful, result:\n{res}')
    return res

@app.get('/meta_files/{file_name}') # дополнить для безопасного пользования. Исключить строки, содержащие
def download_file(file_name: str):
    """Скачивает файл с именем file_name из директории meta_files.
    
    Args:
        file_name (str): имя скачиваемого файла.
    Returns:
        FileResponse"""
    file_path = os.path.join(UPLOAD_DIR, file_name)
    logger.info(f'Func download_file: successful, result:\n{file_name}')
    return FileResponse(path=file_path, media_type='application/octet-stream')

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """Асинхронная функция загрузки файла на трекер.
    
    Args:
        file (UploadFile): содержит информацию о пользовательском файле."""
    os.makedirs("meta_files", exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, 'wb') as f:
        shutil.copyfileobj(file.file, f) # копирует содержимое файла file.file в файл по пути file_path.
    logger.info(f'Func upload_file: successful, result:\n{file.filename}')
    return {'file_name': file.filename}