from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta
import logging
import os
import time
import sys

from config import settings
from database import get_db, create_tables
from models import User, Contract
from schemas import UserLogin, Token, ContractResponse
from auth import verify_password, create_access_token, get_current_user
from file_service import save_uploaded_file
from service_ai import analyze_contract_file
from create_initial_user import ensure_admin_user_exists

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

max_retries = 30
retry_count = 0

while retry_count < max_retries:
    try:
        create_tables()
        logger.info("Banco conectado")
        break
    except Exception as e:
        retry_count += 1
        if retry_count >= max_retries:
            logger.error("Falha ao conectar banco")
            raise
        time.sleep(2)

if ensure_admin_user_exists():
    logger.info("Usuario admin pronto")

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

app = FastAPI(
    title="API de Análise de Contratos",
    description="API para upload e análise automática de contratos usando IA",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/login", response_model=Token, tags=["auth"])
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_data.username).first()
    
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/contracts/upload", response_model=ContractResponse)
async def upload_contract(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        file_path, original_filename, file_content, mime_type = save_uploaded_file(file)
        logger.info(f"Arquivo salvo: {original_filename}")
        
        analysis = analyze_contract_file(file_content, mime_type, file_path)
        
        contract = Contract(
            filename=original_filename,
            file_path=file_path,
            nome_partes=analysis.nome_partes,
            valores_monetarios=analysis.valores_monetarios,
            obrigacoes_principais=analysis.obrigacoes_principais,
            dados_adicionais=analysis.dados_adicionais,
            clausula_rescisao=analysis.clausula_rescisao,
            created_by=current_user.id
        )
        
        db.add(contract)
        db.commit()
        db.refresh(contract)
        
        logger.info(f"Contrato processado: ID {contract.id}")
        return contract
        
    except Exception as e:
        db.rollback()
        logger.error(f"Erro no upload: {str(e)}")
        
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar contrato: {str(e)}"
        )

@app.get("/contracts/{contract_name}", response_model=ContractResponse)
async def get_contract(
    contract_name: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    contract = db.query(Contract).filter(
        Contract.filename == contract_name
    ).first()
    
    if not contract:
        raise HTTPException(
            status_code=404,
            detail="Contrato não encontrado"
        )
    
    return contract


@app.get("/", include_in_schema=False)
async def root():
    return {
        "message": "API de Análise de Contratos",
        "status": "online",
        "admin_user": "admin/admin123"
    }

@app.get("/health", include_in_schema=False)
async def health_check():
    return {"status": "healthy"}

@app.post("/debug/reset-admin", include_in_schema=False)
async def reset_admin_user():
    if ensure_admin_user_exists():
        return {"message": "Usuario admin recriado"}
    else:
        raise HTTPException(status_code=500, detail="Erro ao recriar usuario")

if __name__ == "__main__":
    import uvicorn
    logger.info("Iniciando servidor")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")