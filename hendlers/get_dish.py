from aiogram import F, Router, types
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from bot_config import db

get_dihs_router = Router()


@get_dihs_router.message(Command('get_dish'))
async def get(message: types.Message):
    data = db.fetch("""SELECT name, cost FROM dish ORDER BY
    cost""", ())
    for i in data:
        await message.answer(f'name:{i['name']}\ncost:{i['cost']}')