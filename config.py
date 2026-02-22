import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    OWNER_ID = os.getenv("OWNER_ID")
    TORTOISE_CONFIG = {
        "connections": {"default": "sqlite:///app/data/db.sqlite3"},
        "apps": {
            "models": {
                "models": ["database.structure"],
                "default_connection": "default",
            },
        },
    }
