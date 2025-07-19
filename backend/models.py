from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    contracts = relationship("Contract", back_populates="creator")

class Contract(Base):
    __tablename__ = "contracts"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False, index=True)
    file_path = Column(String(500), nullable=False)
    nome_partes = Column(Text)
    valores_monetarios = Column(Text)
    obrigacoes_principais = Column(Text)
    dados_adicionais = Column(Text)
    clausula_rescisao = Column(Text)
    processed_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, ForeignKey("users.id"))
    
    creator = relationship("User", back_populates="contracts") 