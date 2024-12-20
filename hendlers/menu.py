from aiogram import Router, types
from aiogram.filters import Command

menu_router = Router()


@menu_router.message(Command("menu"))
async def cmd_menu(message: types.Message):
    menu = ("Меню:\n"
            "1. Кофе - 100\n"
            "2. Чай - 50\n"
            "3. Сэндвич - 150\n"
            "4. Суп - 200")
    await message.answer(menu)
