from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = "Для вывода списка проектов, по которым в системе есть расчет " \
           "трудоемкости, нажмите на кнопку 'Посмотреть проекты'"
    
    await message.answer(text)
