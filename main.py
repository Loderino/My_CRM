from CRM.core.database_setup import init_db, verify_database
from CRM.core.engine import async_engine


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
    
    # Здесь будут запускаться другие службы
    # - API сервер
    # - Фоновые задачи
    return True


async def shutdown():
    """Остановка служб при завершении"""
    print("\n🛑 Остановка служб...")
    await async_engine.dispose()
    print("✅ Соединения с БД закрыты")


if __name__ == "__main__":
    import asyncio
    import sys
    try:
        if startup():
            print("\n💡 Приложение готово. Здесь будет основной цикл.")
        else:
            print("\n❌ Ошибка инициализации. Завершение работы.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Получен сигнал прерывания")
    finally:
        # Очистка ресурсов
        asyncio.run(shutdown())
        print("👯 До свидания!")