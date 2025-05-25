from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import getpass

api_id   = int(input("API_ID: "))
api_hash = input("API_HASH: ")
phone    = input("Телефон (+7999…): ")

with TelegramClient(StringSession(), api_id, api_hash) as client:
    client.start(phone=phone, password=getpass.getpass("2FA-пароль (если есть): "))
    print("\nSESSION=" + client.session.save())
