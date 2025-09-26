import os

class ProductionConfig:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    OWNER_ID = os.getenv("OWNER_ID")
    DB_URL = os.getenv("DATABASE_URL", "sqlite:///data/db.sqlite3")
    
    if not all([BOT_TOKEN, OWNER_ID]):
        raise ValueError("Config-value(s) not found.")