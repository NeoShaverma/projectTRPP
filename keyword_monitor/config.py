import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
STRING_SESSION = os.getenv("SESSION")
KEYWORDS = {k.strip().lower() for k in os.getenv("KEYWORDS", "").split(",") if k.strip()}
CHANNELS = [c.strip() for c in os.getenv("CHANNELS", "").split(",") if c.strip()]
THRESHOLD = int(os.getenv("THRESHOLD", 10))
WINDOW_MINUTES = int(os.getenv("WINDOW_MINUTES", 60))
ALERT_CHAT = os.getenv("ALERT_CHAT", "me")
DB_URL = f"sqlite:///{DATA_DIR/'monitor.db'}"
FORWARD_CHAT = os.getenv("FORWARD_CHAT")
