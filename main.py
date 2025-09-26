import asyncio
import signal
import sys

from loguru import logger
from aiogram import Dispatcher

from catching.doc import catch_doc
from catching.text import catch_text
from catching.voice import catch_voice
from catching.video import catch_video
from catching.photo import catch_photo
from catching.deleted import catch_deleted
from catching.destructing_msgs import catch_destructing

from config import Config
from database.structure import close_db, init_db

bot = Config.bot
dp = Dispatcher()

@dp.startup()
async def on_startup():
    logger.debug("Start initialization")

    me = await bot.get_me()

    logger.info(
        f"\nBot @{me.username} initialized\n"
        f"Bot ID: {me.id}\n"
        f"Bot NickName: {me.first_name}\n"
        f"Bot BusinessMode: {me.can_connect_to_business}"
    )

    if me.can_connect_to_business == False:
        logger.error(
            "Bot cant connect to business! Turn ON business mode in @BotFather"
        )
        await bot.session.close()
        return

    await init_db()

    # Without message-object
    dp.include_router(catch_destructing)
    logger.success("[INIT][ROUTERS] Destructing messages initialized")

    dp.include_router(catch_deleted)
    logger.success("[INIT][ROUTERS] Deleted messages initialized")

    # default types
    dp.include_router(catch_photo)
    logger.success("[INIT][ROUTERS] Photo messages initialized")

    dp.include_router(catch_doc)
    logger.success("[INIT][ROUTERS] Doc messages initialized")

    dp.include_router(catch_voice)
    logger.success("[INIT][ROUTERS] Voice messages initialized")

    dp.include_router(catch_video)
    logger.success("[INIT][ROUTERS] Video messages initialized")

    dp.include_router(catch_text)
    logger.success("[INIT][ROUTERS] Text messages initialized")

@dp.shutdown()
async def on_shutdown():
    logger.info("Starting shutdown...")
    
    try:
        await close_db()
    except Exception as e:
        logger.warning(f"Error while closing DB connections: {e}")

    logger.debug('Shutdown completed')

async def main():
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
        logger.info("Cleanup completed")

def signal_handler(signum, frame):
    sys.exit(0)

if __name__ == "__main__":
    """
    Try to graceful-shutdown
    """
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Application terminated gracefully")