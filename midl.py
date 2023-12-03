from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types, Dispatcher


class Callback_mid(BaseMiddleware):
    async def on_process_update(self, update: types.Update, data: dict):
       print(update)


async def registration_midl(dp: Dispatcher):
    dp.middleware.setup(Callback_mid())