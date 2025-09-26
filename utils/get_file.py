import os

from loguru import logger


async def get_file(file_id, bot):
    try:
        logger.info("[UTILS][GET-FILE] Try to receive file")
        file_info = await bot.get_file(file_id)

        logger.debug(f"[UTILS][GET-FILE] File-ID: {file_info.file_id}")

        file_path = file_info.file_path

        project_root = os.path.dirname(os.path.abspath(__file__))

        destination_path = os.path.join(project_root, os.path.basename(file_path))
        logger.debug(
            f"[UTILS][GET-FILE] Absoulte file destination path: {destination_path}"
        )

        await bot.download_file(file_path, destination=destination_path)
        logger.success(
            "[UTILS][GET-FILE] The file was successfully received and downloaded."
        )

        return destination_path

    except Exception as e:
        logger.error(f"[UTILS][GET-FILE] Error when receiving file: {e}")
