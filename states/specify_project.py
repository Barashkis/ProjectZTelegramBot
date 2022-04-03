from aiogram.dispatcher.filters.state import StatesGroup, State


class SpecifyProject(StatesGroup):
    custom = State()
