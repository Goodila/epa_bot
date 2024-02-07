from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, ContentType
import asyncio
import logging
from funcs import get_config

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from handlers import registration_handlers
from midl import registration_midl

config = get_config()
bot = Bot(token=config.token, parse_mode='HTML')
dp = Dispatcher(bot, storage=MemoryStorage())


async def start():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s"
                                                   "(%(filename)s).%(funcName)s,(%(lineno)d) - %(message)s"
                        )

    # регистрируем хендлеры
    registration_handlers(dp)
    # регистрируем мидлвари
    # await registration_midl(dp)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())  