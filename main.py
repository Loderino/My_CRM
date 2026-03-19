import asyncio
import sys
from CRM.core.database_setup import init_db, verify_database
from CRM.core.engine import async_engine
from CRM.server.main import run_server


def startup():
    try:
        init_db()
        print("✅ База данных инициализирована")
    except Exception as e:
        print(f"❌ Ошибка инициализации БД: {e}")
        return False
    
    if not verify_database():
        print("❌ Не удалось подключиться к БД")
        return False
    
    print("✅ Подключение к БД установлено")
    return True


async def shutdown():
    """Остановка служб при завершении"""
    print("\n🛑 Остановка служб...")
    await async_engine.dispose()
    print("✅ Соединения с БД закрыты")


async def main():
    """Главная асинхронная функция"""
    if not startup():
        print("\n❌ Ошибка инициализации. Завершение работы.")
        sys.exit(1)
    
    print("\n🚀 Запуск веб-сервера на http://127.0.0.1:8000")
    try:
        await run_server()
    except KeyboardInterrupt:
        print("\n\n⚠️ Получен сигнал прерывания")
    finally:
        await shutdown()


if __name__ == "__main__":
    asyncio.run(main())
    print("👋 До свидания!")