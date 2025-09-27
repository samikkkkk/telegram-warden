import os

from aiogram import Bot

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    OWNER_ID = os.getenv("OWNER_ID")
    DB_URL = os.getenv("DATABASE_URL")

    bot = Bot(BOT_TOKEN)
    
    if not all([BOT_TOKEN, OWNER_ID]):
        raise ValueError("Config-value(s) not found.")