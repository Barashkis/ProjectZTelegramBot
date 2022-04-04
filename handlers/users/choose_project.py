from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent

from loader import dp, bot

from main import get_data, get_screenshot
from states import SpecifyProject
from dotenv import load_dotenv
from os import getenv


async def auth():
    load_dotenv()

    state = dp.current_state()
    data = await state.get_data()
    user_id = data["user_id"]

    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--start-maximized')
    options.add_argument(f"user-agent={UserAgent().random}")

    s = Service(executable_path=getenv("executable_path"))

    driver = webdriver.Chrome(options=options, service=s)

    try:
        driver.get("https://zvezda.cam-program.ru/logincnc/")

        login_input = driver.find_element(By.NAME, "user_login")
        login_input.send_keys(getenv("login"))

        password_input = driver.find_element(By.NAME, "user_pass")
        password_input.send_keys(getenv("password"))

        driver.find_element(By.CLASS_NAME, "fa-sign-in").click()

        return driver
    except Exception as _ex:
        bot.send_message(user_id, "Что-то пошло не так... Пожалуйста, повторите попытку позже")


@dp.message_handler(Text(equals="Посмотреть проекты"))
async def choose_project_id(message: types.Message, state: FSMContext):
    await message.answer("Извлекаю информацию о всех проектах...")
    driver = await auth()

    all_projects = await get_data(dp, driver)

    driver.close()
    driver.quit()

    await state.update_data({
        "all_projects": all_projects
    })

    await message.answer("Текущий список проектов")
    await message.answer("\n".join([f"{item[0]}. {item[1]}" for item in all_projects.items()]))
    await message.answer("Введите номер проекта, информацию о котором Вы хотите получить")

    await SpecifyProject.custom.set()


@dp.message_handler(state=SpecifyProject.custom)
async def send_project_info(message: types.Message, state: FSMContext):
    await message.answer("Подождите, это займет несколько секунд")

    project_id = int(message.text)
    await state.reset_state(with_data=False)

    data = await state.get_data()
    all_projects = data["all_projects"]
    user_id = data["user_id"]

    await SpecifyProject.custom.set()
    if not (1 <= project_id <= len(all_projects)):
        raise ValueError
    await state.reset_state(with_data=False)

    driver = await auth()

    path = await get_screenshot(dp, driver, project_id)

    driver.close()
    driver.quit()

    await bot.send_document(chat_id=user_id, document=open(path, "rb+"))
