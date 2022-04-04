from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from os import getenv
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent


load_dotenv()


def auth():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
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
        print(_ex)


token = getenv("token")

auth_driver = auth()
memory = MemoryStorage()
bot = Bot(token=token)
dp = Dispatcher(bot, storage=memory)
