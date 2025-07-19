import logging
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from auth import get_password_hash

logger = logging.getLogger(__name__)

def create_initial_admin_user():
    db: Session = SessionLocal()
    
    try:
        admin_user = db.query(User).filter(User.username == "admin").first()
        password_hash = get_password_hash("admin123")
        
        if admin_user:
            admin_user.password_hash = password_hash
            db.commit()
            logger.info("Usuario admin atualizado")
        else:
            new_admin = User(
                username="admin",
                password_hash=password_hash
            )
            db.add(new_admin)
            db.commit()
            logger.info("Usuario admin criado")
            
        return True
        
    except Exception as e:
        logger.error(f"Erro ao criar usuario admin: {e}")
        db.rollback()
        return False
        
    finally:
        db.close()

def ensure_admin_user_exists():
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            if create_initial_admin_user():
                return True
            retry_count += 1
            
        except Exception as e:
            retry_count += 1
            if retry_count >= max_retries:
                logger.error(f"Falha ao criar usuario admin: {e}")
            
        if retry_count < max_retries:
            import time
            time.sleep(1)
    
    return False 