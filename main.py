import logging
import sqlite3
from datetime import datetime, timedelta
import asyncio
from telethon import TelegramClient, events

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Настройки Telethon - замените на свои данные
api_id = 123456         # Замените на ваш API ID
api_hash = 'YOUR_API_HASH'  # Замените на ваш API Hash
session_name = 'user_session'  # Файл сессии для хранения данных авторизации

client = TelegramClient(session_name, api_id, api_hash)

# Инициализация базы данных SQLite для хранения ссылок на посты с маркерными словами
conn = sqlite3.connect('marker_posts.db')
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS marker_posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        channel_id INTEGER,
        message_id INTEGER,
        link TEXT,
        date TEXT
    )
""")
conn.commit()

# Список слов-маркеров
MARKER_WORDS = ["пример", "test", "слово", "маркер"]

# Порог для аномальной активности: если за последние TIME_WINDOW минут количество постов с маркерами превышает MARKER_THRESHOLD
MARKER_THRESHOLD = 5
TIME_WINDOW = 5  # в минутах

# Словарь для отслеживания времени постов с маркерами для каждого канала
marker_activity = {}

def store_marker_post(channel_id, message_id, link, date):
    """Сохраняет ссылку на пост с маркерным словом в базу данных."""
    cursor.execute("""
        INSERT INTO marker_posts (channel_id, message_id, link, date)
        VALUES (?, ?, ?, ?)
    """, (channel_id, message_id, link, date))
    conn.commit()

def contains_marker(text):
    """Проверяет, содержит ли текст хотя бы одно из слов-маркеров."""
    text_lower = text.lower()
    for word in MARKER_WORDS:
        if word.lower() in text_lower:
            return True
    return False

def get_post_link(channel, message):
    """Генерирует публичную ссылку на пост, если это возможно."""
    # Если у канала есть username, используем его для формирования ссылки
    if hasattr(channel, 'username') and channel.username:
        return f"https://t.me/{channel.username}/{message.id}"
    else:
        # Если каналу нет username, пробуем сформировать ссылку в формате t.me/c/<numeric_id>/<message_id>
        # Обычно channel.id имеет формат -100XXXXXXXXX для супергрупп/каналов
        if isinstance(channel.id, int) and str(channel.id).startswith("-100"):
            numeric_id = str(channel.id)[4:]
            return f"https://t.me/c/{numeric_id}/{message.id}"
        else:
            return "Ссылка недоступна"

def add_marker_activity(channel_id, timestamp):
    """Добавляет временную метку поста с маркерным словом для отслеживания активности."""
    if channel_id not in marker_activity:
        marker_activity[channel_id] = []
    marker_activity[channel_id].append(timestamp)

def count_recent_markers(channel_id, current_time):
    """Подсчитывает количество постов с маркерами за последние TIME_WINDOW минут."""
    if channel_id not in marker_activity:
        return 0
    window_start = current_time - timedelta(minutes=TIME_WINDOW)
    # Оставляем только посты за последние TIME_WINDOW минут
    marker_activity[channel_id] = [t for t in marker_activity[channel_id] if t > window_start]
    return len(marker_activity[channel_id])

async def main():
    # Запуск клиента Telethon (вход с аккаунта пользователя)
    await client.start()
    logger.info("Вход выполнен, клиент запущен.")

    @client.on(events.NewMessage())
    async def handler(event):
        # Обрабатываем только сообщения из каналов
        if not event.is_channel:
            return

        channel = await event.get_chat()
        channel_id = channel.id
        message = event.message
        message_text = message.message or ""
        message_id = message.id
        message_date = message.date

        # Проверяем наличие маркерных слов в тексте сообщения
        if contains_marker(message_text):
            # Формируем ссылку на пост
            link = get_post_link(channel, message)
            logger.info(f"Найдено маркерное слово в канале {channel_id}: {message_text}")
            logger.info(f"Ссылка на пост: {link}")

            # Сохраняем ссылку на пост в базу данных
            store_marker_post(channel_id, message_id, link, message_date.isoformat())

            # Отслеживаем аномальную активность по количеству постов с маркерными словами
            add_marker_activity(channel_id, message_date)
            count = count_recent_markers(channel_id, message_date)
            if count >= MARKER_THRESHOLD:
                logger.info(f"Обнаружена аномальная активность в канале {channel_id}: {count} постов с маркерами за последние {TIME_WINDOW} минут.")

    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
