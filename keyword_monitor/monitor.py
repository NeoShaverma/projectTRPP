import asyncio
from datetime import datetime
from pathlib import Path
import pandas as pd
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.channels import JoinChannelRequest

from .anomalies import check_keyword_spikes
from .config import (
    API_ID,
    API_HASH,
    STRING_SESSION,
    KEYWORDS,
    CHANNELS,
    ALERT_CHAT,
    FORWARD_CHAT
)
from .db import init_db, SessionLocal, Message

EXCEL_PATH = Path(__file__).parent.parent / 'data' / 'posts.xlsx'
def create_client() -> TelegramClient:
    return TelegramClient(
        StringSession(STRING_SESSION),
        API_ID,
        API_HASH,
        system_version="4.16.30-vxCUSTOM"  # avoid floodwait bug
    )

async def ensure_channels(client: TelegramClient):
    for ch in CHANNELS:
        try:
            await client(JoinChannelRequest(ch))
        except Exception:
            # already joined or failed, ignore
            pass
def append_to_excel(link: str, channel_tag: str, posted_at: datetime, keywords: list[str]):
    """Добавляет строку в файл posts.xlsx, создаёт его, если не существует."""
    columns = ['link', 'channel_tag', 'posted_at', 'keywords']

    # Убираем tzinfo
    if posted_at.tzinfo is not None:
        posted_at = posted_at.replace(tzinfo=None)

    new_row = {
        'link': link,
        'channel_tag': channel_tag,
        'posted_at': posted_at,
        'keywords': ", ".join(keywords)
    }

    # Если файл не существует — создаём DataFrame с нужными колонками
    if not EXCEL_PATH.exists():
        df = pd.DataFrame([new_row], columns=columns)
    else:
        # Читаем существующий файл
        df = pd.read_excel(EXCEL_PATH)
        # Добавляем новую строку напрямую, избегая pd.concat
        df.loc[len(df)] = [new_row[col] for col in columns]

    # Сохраняем обратно в Excel
    df.to_excel(EXCEL_PATH, index=False)

async def start_monitoring():
    init_db()
    client = create_client()

    @client.on(events.NewMessage(chats=CHANNELS))
    async def handler(event):
        if event.message.fwd_from:
            return
        text = event.message.message.lower()
        matched = [kw for kw in KEYWORDS if kw.lower() in text]
        if not matched:
            return
        for kw in KEYWORDS:
            if kw.lower() in text:
                # 1) переслать оригинал в ваш канал
                await client.forward_messages(
                    entity=FORWARD_CHAT,  # куда переслать
                    messages=event.message,  # что переслать
                    from_peer=event.chat_id  # откуда
                )
                link = (
                    event.message.link
                    if hasattr(event.message, 'link')
                    else f"https://t.me/{event.chat.username or event.chat_id}/{event.message.id}"
                )
                # Тэг канала (username или chat_id)
                channel_tag = event.chat.username or str(event.chat_id)
                # Время публикации (datetime)
                posted_at = event.message.date
                # 2. Запись в БД
                session = SessionLocal()
                try:
                    msg = Message(
                        channel_id=event.chat_id,
                        message_id=event.message.id,
                        date=event.message.date,
                        text=event.raw_text,
                        keywords=[kw]
                    )
                    session.add(msg)
                    session.commit()
                except Exception as e:
                    session.rollback()
                    print(f"DB error: {e}")
                finally:
                    session.close()
                try:
                    append_to_excel(
                        link=link,
                        channel_tag=channel_tag,
                        posted_at=posted_at,
                        keywords=matched
                    )
                except Exception as e:
                    print(f"Excel write error: {e}")
                break

        spikes = check_keyword_spikes(event.chat_id)
        if spikes:
            alert_lines = [f"⚠️ Spike in {kw}: {cnt} msgs" for kw, cnt in spikes]
            await client.send_message(ALERT_CHAT, "\n".join(alert_lines))

    async with client:
        await ensure_channels(client)
        print("[Monitor] Started. Listening for messages...")
        await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(start_monitoring())
