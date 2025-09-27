import os

from aiogram import Bot

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    OWNER_ID = os.getenv("OWNER_ID")
    TORTOISE_CONFIG = {
    "connections": {
        "default": "sqlite:///app/data/db.sqlite3"
        },
        
    "apps": {
        "models": {
            "models": ["database.structure"],
            "default_connection": "default",
        },
    },
}


    bot = Bot(BOT_TOKEN)
    
    if not all([BOT_TOKEN, OWNER_ID]):
        raise ValueError("Config-value(s) not found.")