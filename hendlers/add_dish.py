from aiogram import F, Router, types
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import ContentType
from bot_config import db

add_dish_router = Router()

add_dish_router.message.filter(
    F.from_user.id == 7584394670
)


class Dish(StatesGroup):
    name = State()
    cost = State()
    description = State()
    category = State()
    image = State()
    status = State()


@add_dish_router.message(Command('add_dish'), default_state)
async def creat_dish(message: types.Message, state: FSMContext):
    await state.set_state(Dish.name)
    await message.answer('Назовите блюдо')


@add_dish_router.message(Dish.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name_dish=message.text)
    await state.set_state(Dish.cost)
    await message.answer("Какая цена")


@add_dish_router.message(Dish.cost)
async def process_cost(message: types.Message, state: FSMContext):
    await state.update_data(cost_dish=message.text)
    await message.answer("Опишите блюдо")
    await state.set_state(Dish.description)


@add_dish_router.message(Dish.description)
async def process_description(message: types.Message, state: FSMContext):
    await state.update_data(description_dish=message.text)
    await message.answer("Назовите категорию блюда")
    await state.set_state(Dish.category)


@add_dish_router.message(Dish.category)
async def process_category(message: types.Message, state: FSMContext):
    await state.update_data(category_dish=message.text)
    await message.answer('Теперь отправьте изображение блюда')
    await state.set_state(Dish.image)


@add_dish_router.message(Dish.image, F.content_type == ContentType.PHOTO)
async def process_image(message: types.Message, state: FSMContext):
    photo = message.photo[-1]
    photo_id = photo.file_id
    await state.update_data(image_dish=photo_id)
    await message.answer('Подтверждаете ли вы добавление блюда? (y/n)')
    await state.set_state(Dish.status)


@add_dish_router.message(Dish.image)
async def process_invalid_image(message: types.Message):
    await message.answer("Пожалуйста, отправьте изображение в формате фото")


@add_dish_router.message(Dish.status)
async def process_status(message: types.Message, state: FSMContext):
    if message.text.lower() == 'y':
        data = await state.get_data()
        name_dish = data.get('name_dish')
        cost_dish = data.get('cost_dish')
        description_dish = data.get('description_dish')
        category_dish = data.get('category_dish')
        image_dish = data.get('image_dish')
        if not all([name_dish, cost_dish, description_dish, category_dish, image_dish]):
            await message.answer("Некоторые данные отсутствуют. Проверьте ввод.")
            return

        try:

            db.execute(
                "INSERT INTO dish (name_dish, cost_dish, description_dish, category_dish, image_dish) VALUES (?, ?, ?, ?, ?)",
                (name_dish, cost_dish, description_dish, category_dish, image_dish)
            )
            await message.answer("Блюдо успешно добавлено в базу данных!")
            await state.clear()
        except Exception as e:
            await message.answer(f"Произошла ошибка при добавлении блюда: {e}")
    elif message.text.lower() == 'n':
        await message.answer('Добавление блюда отменено.')
        await state.clear()
    else:
        await message.answer('Введите "y" или "n"!')
