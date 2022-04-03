from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard = ReplyKeyboardMarkup([
    [
        KeyboardButton(text="Посмотреть проекты")
    ],
],
    resize_keyboard=True
)
