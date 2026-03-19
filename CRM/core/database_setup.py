import subprocess
import os

from sqlalchemy import create_engine, text
from sqlalchemy_utils import database_exists, create_database

from CRM.core.config import settings

def ensure_database_exists():
    """Проверяет существование БД и создаёт её"""
    db_url = settings.database_url.replace("+asyncpg", "")
    
    try:
        if not database_exists(db_url):
            create_database(db_url)
            print(f"✅ База данных '{settings.DB_NAME}' создана")
        return True
    except Exception as e:
        print(f"❌ Ошибка создания БД: {e}")
        return False

def run_migrations():
    """Запускает миграции Alembic"""
    try:
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(__file__))
        )
        
        if result.returncode == 0:
            print("✅ Миграции успешно применены")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print(f"❌ Ошибка миграций: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Ошибка запуска миграций: {e}")
        return False

def init_db():
    """Полная инициализация: создание БД + миграции"""
    if not ensure_database_exists():
        raise Exception("Не удалось создать базу данных")
    
    if not run_migrations():
        raise Exception("Не удалось применить миграции")
    
    print("✅ База данных полностью инициализирована")
    return True

def verify_database():
    """Проверка доступности БД"""
    try:
        engine = create_engine(settings.database_url.replace("+asyncpg", ""))
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"❌ Ошибка подключения к БД: {e}")
        return False