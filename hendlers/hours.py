from aiogram import Router, types
from aiogram.filters import Command

hours_router = Router()


@hours_router.message(Command("hours"))
async def cmd_hours(message: types.Message):
    hours = ("Часы работы:\n"
    "Пн-Пт: 9:00 - 21:00\n"
    "Сб-Вс: 10:00 - 22:00")

    await message.answer(hours)
