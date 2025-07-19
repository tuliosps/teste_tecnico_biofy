import os
from typing import Tuple
from fastapi import UploadFile, HTTPException
from config import settings
import uuid

def save_uploaded_file(file: UploadFile) -> Tuple[str, str, bytes, str]:
    #os.makedirs(settings.UPLOAD_DIR, exist_ok=True) #deixei aqui so pra caso queria criar a pasta automaticamente.
    
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400, 
            detail=f"Tipo de arquivo não suportado. Use: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )
    
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
    
    try:
        content = file.file.read()
        
        if len(content) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400, 
                detail=f"Arquivo muito grande. Máximo: {settings.MAX_FILE_SIZE // (1024*1024)}MB"
            )
        
        with open(file_path, "wb") as buffer:
            buffer.write(content)
        
        mime_type = "application/pdf" if file_extension == ".pdf" else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        
        return file_path, file.filename, content, mime_type
        
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Erro ao salvar arquivo: {str(e)}")