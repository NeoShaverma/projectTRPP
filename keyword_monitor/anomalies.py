from datetime import datetime, timedelta
from sqlalchemy import select, func
from .db import SessionLocal, Message
from .config import THRESHOLD, WINDOW_MINUTES, KEYWORDS

def check_keyword_spikes(channel_id: int) -> list[str]:
    """Return list of keywords whose count exceeds THRESHOLD."""
    cutoff = datetime.utcnow() - timedelta(minutes=WINDOW_MINUTES)
    alerts = []
    with SessionLocal() as db:
        for kw in KEYWORDS:
            stmt = (
                select(func.count())
                .where(
                    Message.channel_id == channel_id,
                    Message.keywords.contains([kw]),
                    Message.date >= cutoff,
                )
            )
            count = db.scalar(stmt)
            if count and count >= THRESHOLD:
                alerts.append((kw, count))
    return alerts
