import os
import config

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Update

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from fake_useragent import UserAgent
from typing import Optional

from loader import dp

from main import get_data, get_screenshot


async def get_auth_driver() -> Optional[webdriver.Chrome]:
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

    s = Service(executable_path=config.executable_path)

    driver = webdriver.Chrome(options=options, service=s)

    try:
        driver.get("https://zvezda.cam-program.ru/logincnc")

        login_input = driver.find_element(By.NAME, "user_login")
        login_input.send_keys(config.login)

        password_input = driver.find_element(By.NAME, "user_pass")
        password_input.send_keys(config.password)

        driver.find_element(By.CLASS_NAME, "fa-sign-in").click()
    except Exception as _ex:
        driver.close()
        driver.quit()

        return
    else:
        return driver


@dp.message_handler(Text(equals="Посмотреть проекты"))
async def choose_project_id(message: types.Message, state: FSMContext):
    await message.answer("Извлекаю информацию о всех проектах...")

    auth_driver = await get_auth_driver()

    try:
        all_projects = await get_data(auth_driver)
    except Exception:
        await message.answer("Что-то пошло не так... Пожалуйста, повторите попытку позже")
    else:
        await message.answer("\n".join([f"{item[0]}. {item[1]}" for item in all_projects.items()]))
        await message.answer("Введите номер проекта, информацию о котором Вы хотите получить")

        await state.set_state("specify_project")
        await state.update_data({
            "all_projects": all_projects
        })
    finally:
        if auth_driver is not None:
            auth_driver.close()
            auth_driver.quit()


@dp.message_handler(state="specify_project")
async def send_project_info(message: types.Message, state: FSMContext):
    project_id = int(message.text)

    data = await state.get_data()
    all_projects = data["all_projects"]
    if not (1 <= project_id <= len(all_projects)):
        raise ValueError

    await message.answer("Подождите, это займет несколько секунд")

    auth_driver = await get_auth_driver()

    try:
        path = await get_screenshot(dp, auth_driver, project_id)
    except Exception:
        await message.answer("Что-то пошло не так... Пожалуйста, повторите попытку позже")
    else:
        await message.answer_document(document=open(path, "rb+"))
        os.remove(path)
    finally:
        if auth_driver is not None:
            auth_driver.close()
            auth_driver.quit()

        await state.finish()
