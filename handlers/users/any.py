from aiogram import types
from aiogram.types import ContentType

from loader import dp


@dp.message_handler(content_types=ContentType.ANY)
async def send_message(message: types.Message):
    await message.reply("К сожалению, у меня нет ответа на это сообщение... "
                        "Чтобы взаимодействовать со мной, используйте кнопку и команды /start и /help")
