from aiogram import F, Router, types
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from bot_config import db

add_dish_router = Router()

add_dish_router.message.filter(
    F.from_user.id == 7584394670
)

class Dish(StatesGroup):
    name = State()
    cost = State()

@add_dish_router.message(Command('add_dish'), default_state)
async def creat_dish(message: types.Message, state: FSMContext):
    await state.set_state(Dish.name)
    await message.answer('Названия блюдо')

@add_dish_router.message(Dish.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Dish.cost)
    await message.answer("Какая цена")

@add_dish_router.message(Dish.cost)
async def process_cost(message: types.Message, state: FSMContext):
    await state.update_data(cost=message.text)
    data = await state.get_data()
    db.execute("""INSERT INTO dish VALUES(?,?,?)""", (None, data['name'], data['cost']))
    await message.answer('Хорошо ваша еда добавлена')
    await state.clear()