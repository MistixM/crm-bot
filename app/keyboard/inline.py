# --
# Inline keyboard generator. 
# Create all the necessary inline keyboards here
# --
from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def reply_button(user_id: int, account_name: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f'Reply from {account_name}', callback_data=f'reply_{user_id}_{account_name}')]
        ])