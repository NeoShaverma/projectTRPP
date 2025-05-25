import asyncio
from .monitor import start_monitoring
from keyword_monitor.db import init_db

init_db()  # создаст таблицу messages, если ещё нет
if __name__ == "__main__":
    asyncio.run(start_monitoring())
