from aiogram.types import Update

from loader import dp


@dp.errors_handler()
async def catch_errors(update: Update, exception):
    if isinstance(exception, ValueError):
        state = dp.current_state()
        data = await state.get_data()
        all_projects = data["all_projects"]

        await update.get_current().message.answer(f"Необходимо ввести число "
                                                  f"от 1 до {len(all_projects)}! Попробуйте ещё раз")
