# --
# In this module the bot stores client data
# --
from telethon import TelegramClient

from app.constants.config import accounts

clients = []
account_names = [] # this will be used later.. delete with caution


# Iterate and append each client to the list
for account in accounts:
    client = TelegramClient(
        session=account['session_name'], 
        api_id=account['api_id'], 
        api_hash=account['api_hash']
    )

    clients.append(client)