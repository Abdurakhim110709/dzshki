from aiogram import F, Router, types
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from bot_config import db

get_dihs_router = Router()


@get_dihs_router.message(Command('get_dish'))
async def get(message: types.Message):
    dishes = db.fetch("SELECT * FROM dish")
    for i in dishes:
        await message.answer(f'name: {i["name_dish"]}\ncost: {i["cost_dish"]}\ndescription: {i["description_dish"]}\ncategory: {i["category_dish"]}')
