from sqlalchemy import create_engine, text
from sqlalchemy_utils import database_exists, create_database
from CRM.core.config import settings
from CRM.core.engine import Base

def ensure_database_exists():
    db_url = settings.database_url.replace("+asyncpg", "")

    try:
        if not database_exists(db_url):
            create_database(db_url)
        return True
    except Exception as e:
        print(e)
        return False

def init_db():
    if not ensure_database_exists():
        raise Exception("Не удалось создать базу данных")
    
    engine = create_engine(settings.database_url.replace("+asyncpg", ""))
    Base.metadata.create_all(bind=engine)
    return True

def verify_database():
    try:
        engine = create_engine(settings.database_url.replace("+asyncpg", ""))
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False