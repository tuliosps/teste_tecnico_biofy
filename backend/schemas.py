from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class UserLogin(BaseModel):
    username: str = Field(..., example="admin")
    password: str = Field(..., example="admin123")
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "admin",
                "password": "admin123"
            }
        }

class Token(BaseModel):
    access_token: str
    token_type: str

class ContractResponse(BaseModel):
    id: int
    filename: str
    nome_partes: Optional[str] = None
    valores_monetarios: Optional[str] = None
    obrigacoes_principais: Optional[str] = None
    dados_adicionais: Optional[str] = None
    clausula_rescisao: Optional[str] = None
    
    class Config:
        from_attributes = True

class ContractAnalysis(BaseModel):
    nome_partes: str
    valores_monetarios: str
    obrigacoes_principais: str
    dados_adicionais: str
    clausula_rescisao: str 