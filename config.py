import os
import json

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEYWORDS_FILE = os.path.join(BASE_DIR, "keywords.json")
DB_PATH = os.path.join(BASE_DIR, "database/concursos.db")

# Load Keywords
with open(KEYWORDS_FILE, 'r', encoding='utf-8') as f:
    CONFIG_DATA = json.load(f)

KEYWORDS = CONFIG_DATA.get('keywords', {})
SCORES = CONFIG_DATA.get('scores', {})
PRIORITIES = CONFIG_DATA.get('priorities', {})

# Scraper Settings
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# Notification Settings (Placeholders)
EMAIL_SENDER = os.getenv("EMAIL_SENDER", "seu_email@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "sua_senha")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER", "seu_email@gmail.com")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
