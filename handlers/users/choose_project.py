import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Update

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent

from loader import dp, bot

from dotenv import load_dotenv

from main import get_data, get_screenshot
from states import SpecifyProject


async def auth():
    load_dotenv()

    state = dp.current_state()
    data = await state.get_data()
    user_id = data.get("user_id")

    if user_id is None:
        await state.update_data({
            "user_id": Update.get_current().message.from_user.id
        })

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--start-maximized')
    options.add_argument(f"user-agent={UserAgent().random}")

    s = Service(executable_path=os.getenv("executable_path"))

    driver = webdriver.Chrome(options=options, service=s)

    try:
        driver.get("https://zvezda.cam-program.ru/logincnc/")

        login_input = driver.find_element(By.NAME, "user_login")
        login_input.send_keys(os.getenv("login"))

        password_input = driver.find_element(By.NAME, "user_pass")
        password_input.send_keys(os.getenv("password"))

        driver.find_element(By.CLASS_NAME, "fa-sign-in").click()

        return driver
    except Exception as _ex:
        bot.send_message(user_id, "Что-то пошло не так... Пожалуйста, повторите попытку позже")


@dp.message_handler(Text(equals="Посмотреть проекты"))
async def choose_project_id(message: types.Message):
    await message.answer("Извлекаю информацию о всех проектах...")

    auth_driver = await auth()
    all_projects = await get_data(dp, auth_driver)
    auth_driver.close()
    auth_driver.quit()

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

    auth_driver = await auth()
    path = await get_screenshot(dp, auth_driver, project_id)
    auth_driver.close()
    auth_driver.quit()

    await bot.send_document(chat_id=user_id, document=open(path, "rb+"))
    os.remove(path)
