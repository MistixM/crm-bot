# --
# This script is used for the message sending
# --
from aiogram import Router, types
from aiogram.types import CallbackQuery

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.utils.telethon_client import clients

handler_message = Router()

# It's important to have States for the bot.
# If you want to add additional input functionality:
# 1. Add state into the class
# 2. Add state handler after the callback_query handler
class States(StatesGroup):
    wrt_message = State()


# Handles inline keyboard callback
# If you want to add more callbacks, please remove lambda checking
# and filter incoming data manually
@handler_message.callback_query(lambda d: d.data.startswith('reply_'))
async def handle_callbacks(callback: CallbackQuery, state: FSMContext):
    _, sender_id, account_name = callback.data.split('_')
    account_index = account_name.index(account_name)

    # It's necessary to save the data to the state storage
    await state.update_data(sender_id=sender_id, account_index=account_index)

    await callback.answer() # used for user's input

    await state.set_state(States.wrt_message)
    await callback.message.answer(text=f"Пожалуйста напишите сообщение: {sender_id} (от {account_name}):")

# --
# Add your state handlers here
# --

# This handler is used for the answering to sender
@handler_message.message(States.wrt_message)
async def handle_write_message(msg: types.Message, state: FSMContext):
    # Get all necessary data here
    data = await state.get_data()
    sender_id = int(data.get('sender_id'))
    account_index = data['account_index']

    if msg.text == '/stop':
        await msg.answer(f"Отмена ответа.")
        await state.clear()
        return
    
    # It's optinal, but I added sender_id checking.. 
    if sender_id:
        try:
            await clients[account_index].send_message(sender_id, msg.text)
            await msg.answer(text='Сообщение отправлено!')
    
        except Exception as e:
            await msg.answer(text=f"Ошибка при отправке сообщения: {e}")

    else:
        await msg.answer(text=f"Невозможно найти ID получателя")


    await state.clear()