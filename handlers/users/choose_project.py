from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from loader import dp, bot, auth_driver

from main import get_data, get_screenshot
from states import SpecifyProject


@dp.message_handler(Text(equals="Посмотреть проекты"))
async def choose_project_id(message: types.Message, state: FSMContext):
    await message.answer("Извлекаю информацию о всех проектах...")

    all_projects = await get_data(dp, auth_driver)

    await state.update_data({
        "all_projects": all_projects
    })

    await message.answer("Текущий список проектов")
    await message.answer("\n".join([f"{item[0]}. {item[1]}" for item in all_projects.items()]))
    await message.answer("Введите номер проекта, информацию о котором Вы хотите получить")

    await SpecifyProject.custom.set()


@dp.message_handler(state=SpecifyProject.custom)
async def send_project_info(message: types.Message, state: FSMContext):
    project_id = int(message.text)
    await state.reset_state(with_data=False)

    data = await state.get_data()
    all_projects = data["all_projects"]
    user_id = data["user_id"]

    await SpecifyProject.custom.set()
    if not (1 <= project_id <= len(all_projects)):
        raise ValueError
    await state.reset_state(with_data=False)

    await message.answer("Подождите, это займет несколько секунд")
    path = await get_screenshot(dp, auth_driver, project_id)
    await bot.send_document(chat_id=user_id, document=open(path, "rb+"))
