from telethon import TelegramClient, events

api_id = YOUR_API_ID
api_hash = 'YOUR_API_HASH'
target = 'target_username'

client = TelegramClient('session_name', api_id, api_hash)

keywords = ['ключевое_слово1', 'ключевое_слово2']

@client.on(events.NewMessage())
async def new_message_handler(event):
    if event.is_channel:
        message_text = event.message.message
        if any(keyword.lower() in message_text.lower() for keyword in keywords):
            print(f"Найдено сообщение с ключевым словом: {message_text}")
            await client.forward_messages(target, event.message)

client.start()
print("Бот запущен и ждёт новых сообщений...")
client.run_until_disconnected()
