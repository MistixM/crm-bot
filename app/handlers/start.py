# --
# Just simple start file that handles /start command
# --
from aiogram import Bot, types, Router
from aiogram.filters import CommandStart

from app.constants import config

start_router = Router()

@start_router.message(CommandStart())
async def handle_start(msg: types.Message):
    if not msg.chat.id == config.OWNER_ID:
        await msg.answer(text='Извините, но вам не разрешено пользоваться ботом.')
        return

    await msg.answer(text='Привет! Я помогу в аккаунт менеджменте')