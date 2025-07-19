import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    UPLOAD_DIR = "uploads"
    MAX_FILE_SIZE = 10 * 1024 * 1024
    ALLOWED_EXTENSIONS = {".pdf", ".docx"}

settings = Settings()

if not settings.GEMINI_API_KEY:
    print("   AVISO: Token do Gemini não configurado.")
    print("   Para análise completa, configure GEMINI_API_KEY no arquivo .env")
    print("   Obtenha sua chave em: https://makersuite.google.com/app/apikey")