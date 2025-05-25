        # Keyword Monitor Bot (Telethon)

        This project implements a **Telegram user‑bot** that monitors one or more
        channels for a list of keywords, stores matching posts in SQLite, and
        notifies you when the frequency of any keyword exceeds a configurable
        threshold within a rolling time window.

        ## Features

        * Works **without admin rights** in the channel — acts as a normal user
          via MTProto (Telethon).
        * Simple anomaly detection: if a keyword appears `THRESHOLD` times during
          the last `WINDOW_MINUTES`, you get an alert.
        * All matches are stored in SQLite (`data/monitor.db`).
        * Docker‑ready: `docker-compose up -d` and you're done.

        ## Quick start

        1. **Generate a string session** (first‑time only):

           ```bash
           docker run -it --rm -e API_ID=<id> -e API_HASH=<hash>               -v $(pwd)/session:/app/session               python:3.12-slim python - << 'PY'
           from telethon.sync import TelegramClient
           from telethon.sessions import StringSession
           import os, getpass
           api_id = int(os.environ["API_ID"])
           api_hash = os.environ["API_HASH"]
           phone = input("Phone: ")
           with TelegramClient(StringSession(), api_id, api_hash) as client:
               client.start(phone=phone)
               print("Your STRING_SESSION:
", client.session.save())
           PY
           ```

           Put the printed line into `.env` → `SESSION=`.

        2. **Configure `.env`** – copy `.env.example` and fill the values.

        3. **Run**:

           ```bash
           docker-compose up -d
           ```

        4. **Watch logs**:

           ```bash
           docker-compose logs -f
           ```

        ## Environment variables

        | Variable          | Description                                   |
        |-------------------|-----------------------------------------------|
        | `API_ID`          | Telegram API ID from <https://my.telegram.org>|
        | `API_HASH`        | Telegram API hash                             |
        | `SESSION`         | String session obtained in step 1             |
        | `KEYWORDS`        | Comma‑separated list (e.g. `python,ai`)       |
        | `CHANNELS`        | Comma‑separated usernames or IDs              |
        | `THRESHOLD`       | Integer, messages per window to trigger alert |
        | `WINDOW_MINUTES`  | Rolling window size in minutes                |
        | `ALERT_CHAT`      | Where to send alerts (`me` ⇒ Saved Messages)  |

        ## Project structure

        ```text
        keyword_monitor_bot/
        ├── docker-compose.yml
        ├── Dockerfile
        ├── requirements.txt
        ├── .env.example
        ├── README.md
        └── keyword_monitor/
            ├── __init__.py
            ├── config.py
            ├── db.py
            ├── anomalies.py
            ├── monitor.py
            └── run.py
        ```
