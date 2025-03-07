# --
# This bot was developed for automation purposes only
# --

import asyncio

from aiogram import Bot, Dispatcher

from telethon import events

from app.handlers import routers
from app.keyboard.inline import reply_button
from app.constants import config

from app.utils.telethon_client import clients, account_names


# Initialize telegram bot
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()
dp.include_routers(*routers)


# Handle incoming messages
async def handle_message(client, event, account_name: str):
    # Get all necessary infor about sender
    sender = await event.get_sender()
    sender_full_name = f"{sender.first_name or ''} {sender.last_name or ''}".strip()
    sender_username = f'@{sender.username}' if sender.username else "No useraname"
    sender_id = sender.id
    message = event.message.text

    # Ensure that it is not group
    if not '-' in str(sender_id):
        await bot.send_message(chat_id=config.OWNER_ID,
                            text=f"New message from {sender_full_name} ({sender_username})\n\n{message}",
                            reply_markup=reply_button(sender_id, account_name),
                            )


async def main():
    # Iterate and start each client
    for client in clients:
        await client.start()
        me = await client.get_me()

        account_names.append(me.first_name or me.username or "Account")

        # Create listener for the incoming client message
        @client.on(events.NewMessage)
        async def _(event, client=client, account_name=me.first_name):
            await handle_message(client, event, account_name)

    # Start tg bot
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        print("Bot started.")
        asyncio.run(main())
        
    except (SystemError, KeyboardInterrupt):
        print("Bot stopped.")