

from pathlib import Path
import time
import uuid
from fastapi import UploadFile


class FileManipulator():
    
    @staticmethod
    def save_file_to_local(file : UploadFile, folder_name : str):
        upload_dir = Path(folder_name)
        upload_dir.mkdir(parents=True, exist_ok=True)
        file_extension  = file.filename.split(".")[-1].lower()
        unique_filename = f"{int(time.time())}_{uuid.uuid4().hex[:8]}.{file_extension}"
        file_path = upload_dir / unique_filename
        with file_path.open("wb") as buffer:
            buffer.write(file.file.read()) 
        return str(file_path)