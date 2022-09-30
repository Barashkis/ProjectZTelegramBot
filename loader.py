from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from os import getenv
from dotenv import load_dotenv

load_dotenv()

token = getenv("TOKEN")

memory = MemoryStorage()
bot = Bot(token=token)
dp = Dispatcher(bot, storage=memory)
