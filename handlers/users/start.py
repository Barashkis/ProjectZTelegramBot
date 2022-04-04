from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp

from keyboards import keyboard


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Приветствую, {message.from_user.full_name}!\n\n"
                         "Это Autobot системы CAM-PROGRAM. Здесь Вы можете оперативно посмотерть "
                         "предварительные расчеты трудоемкости изготовления деталей по текущим проектам\n\n"
                         "Воспользуйтесь командой /help, чтобы получить справку", reply_markup=keyboard)
