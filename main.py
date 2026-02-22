import asyncio
import signal
import sys

from loguru import logger
from aiogram import Bot, Dispatcher

from catching.doc import catch_doc
from catching.text import catch_text
from catching.voice import catch_voice
from catching.video import catch_video
from catching.photo import catch_photo
from catching.deleted import catch_deleted
from catching.destructing_msgs import catch_destructing

from config import Config
from database.structure import close_db, init_db

dp = Dispatcher()

@dp.startup()
async def on_startup(bot: Bot):
    logger.debug("Start initialization")

    me = await bot.get_me()
    logger.info(
        f"\nBot @{me.username} initialized\n"
        f"Bot ID: {me.id}\n"
        f"Bot NickName: {me.first_name}\n"
        f"Bot BusinessMode: {me.can_connect_to_business}"
    )

    if not me.can_connect_to_business:
        logger.error("Turn ON business mode in @BotFather")
        await bot.session.close()
        return

    # Регистрация роутеров
    dp.include_router(catch_destructing)
    dp.include_router(catch_deleted)
    dp.include_router(catch_photo)
    dp.include_router(catch_doc)
    dp.include_router(catch_voice)
    dp.include_router(catch_video)
    dp.include_router(catch_text)

    logger.success("[INIT] All routers registered")

@dp.shutdown()
async def on_shutdown(bot: Bot):
    logger.info("Starting shutdown...")
    await close_db()
    logger.debug("Shutdown completed")

async def main():
    bot = Bot(token=Config.BOT_TOKEN)

    await init_db()

    try:
        await dp.start_polling(
            bot,
            handle_signals=True,
            close_bot_session=True,
            allowed_updates=dp.resolve_used_update_types()
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        await bot.session.close()
        logger.info("Cleanup completed")

def signal_handler(signum, frame):
    sys.exit(0)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Application terminated gracefully")