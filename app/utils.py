import re
import uuid
from datetime import datetime, timedelta, timezone

# Regex to remove unwanted characters (keep only letters, numbers, spaces)
RE_CLEAN = re.compile(r"[^a-zA-Z0-9\s]+")


# Define IST timezone (UTC+05:30)
IST = timezone(timedelta(hours=5, minutes=30))


def clean_text(text: str) -> str:
    """Clean input text by removing punctuation/special characters and normalizing spaces."""
    if not text:
        return ""
    t = text.strip()
    t = RE_CLEAN.sub("", t)  # remove punctuation/specials
    t = re.sub(r"\s+", " ", t)  # collapse multiple spaces
    return t.strip()


def make_id() -> str:
    """Generate a unique UUID string."""
    return str(uuid.uuid4())


def ist_now_iso() -> str:
    """Return current time in IST as ISO 8601 string with +05:30 offset."""
    return datetime.now(IST).isoformat()
