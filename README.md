 Telegram Мониторинг Каналов с Маркерными Словами

Этот проект представляет собой Telegram-бота, написанного на Python с использованием библиотеки [Telethon](https://github.com/LonamiWebs/Telethon). Бот выполняет вход с аккаунта пользователя и мониторит каналы, на которые вы подписаны. Он обнаруживает посты, содержащие заданные слова-маркеры, генерирует ссылки на эти посты и сохраняет их в базу данных SQLite. Кроме того, бот отслеживает аномальную активность, если количество постов с маркерами за короткий промежуток времени превышает заданный порог.

 Функциональность

- Вход с аккаунта пользователя: авторизация через Telethon для доступа ко всем каналам, на которые вы подписаны.
- Обнаружение слов-маркеров: поиск заданных слов-маркеров в новых постах.
- Генерация ссылок: формирование публичной ссылки на пост вместо сохранения полного текста сообщения.
- Обнаружение аномальной активности: отслеживание количества постов с маркерными словами за определённое время.
- Хранение данных: сохранение информации о постах (идентификатор канала, идентификатор сообщения, ссылка и дата) в базу данных SQLite (`marker_posts.db`).

 Зависимости

- Python 3.7+
- [Telethon](https://github.com/LonamiWebs/Telethon)  
  Установить можно с помощью:
  pip install telethon