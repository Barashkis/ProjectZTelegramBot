from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp

from keyboards import keyboard


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get("user_id")

    if user_id is None:
        await state.update_data({
            "user_id": message.from_user.id
        })

    await message.answer(f"Приветствую, {message.from_user.full_name}!\n\n"
                         "Это Autobot системы CAM-PROGRAM. Здесь Вы можете оперативно посмотерть "
                         "предварительные расчеты трудоемкости изготовления деталей по текущим проектам\n\n"
                         "Воспользуйтесь командой /help, чтобы получить справку", reply_markup=keyboard)
