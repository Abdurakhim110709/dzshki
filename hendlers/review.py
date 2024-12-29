from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from bot_config import db
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardRemove

# from bot_config import database

review_router = Router()

ratings = {
    'bad' : 2,
    'good' : 5
}

class Review(StatesGroup):
    name = State()
    number_inst = State()
    visit_date = State()
    food_rating = State()
    cleanliness_rating = State()
    extra_comments = State()
    confirm = State()


@review_router.callback_query(F.data == 'review')
async def start_review(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Как вас зовут?')
    await call.message.edit_reply_markup(reply_markup=None)
    await state.set_state(Review.name)


@review_router.message(Review.name)
async def process_name(message: types.Message, state: FSMContext):
    if message.text == message.text.title():
        await state.update_data(name=message.text)
        await message.answer('Ваш номер или инстаграм')
        await state.set_state(Review.number_inst)
    else:
        await message.answer("Напиши с большой буквой!!")
        await state.set_state(Review.name)

@review_router.message(Review.number_inst)
async def process_inst_number(message: types.Message, state: FSMContext):
    await message.answer('когда вы придёте?')
    await state.update_data(number_inst=message.text)
    await state.set_state(Review.visit_date)

@review_router.message(Review.visit_date)
async def process_visit_date(message: types.Message, state: FSMContext):
    kb = types.ReplyKeyboardMarkup(
        keyboard=
        [
        [
            types.KeyboardButton(text='bad', callback_data='bad'),
            types.KeyboardButton(text='good', callback_data='good')

        ]
        ]
                                  )

    await message.answer('оцените еду', reply_markup=kb)
    await state.update_data(visit_date=message.text)
    await state.set_state(Review.food_rating)


@review_router.message(Review.food_rating)
async def process_food_rating(message: types.Message, state: FSMContext):
    kb = types.ReplyKeyboardRemove(keyboard=[
           [
           types.KeyboardButton(text='bad', callback_data='bad'),
           types.KeyboardButton(text='good', callback_data='good'),

            ]
        ]
    )
    if message.text in ('bad', 'good'):
        await state.update_data(food_rating=message.text)
        await message.answer('Как оцениваете чистоту заведения?', reply_markup=kb)
        await state.set_state(Review.cleanliness_rating)
    else:
        await message.answer('Нажмите на кнопки!')
        await state.set_state(Review.food_rating)

@review_router.message(Review.cleanliness_rating)
async def process_cleanliness_rating(message: types.Message, state: FSMContext):
        kb = types.ReplyKeyboardRemove()
        if message.text in ('bad', 'good'):
            await state.update_data(clean=message.text)
            await message.answer('Дополнительные коментарии/Жалобы?', reply_markup=kb)
            await state.set_state(Review.extra_comments)
        else:
            await message.answer('Нажмите на кнопки!')

@review_router.message(Review.extra_comments)
async def process_extra(message: types.Message, state: FSMContext):

    await state.update_data(extra_comments=message.text)
    await message.answer('Потверждете ли вы?(y/n)')
    await state.set_state(Review.confirm)

@review_router.message(Review.confirm)
async def process_confirm(message: types.Message, state: FSMContext):
    if message.text == 'y':
        data = await state.get_data()
        await message.answer(f'{data}\n\nСпасибо за отзыв!!')
        db.execute("""INSERT INTO review VALUES
        (?,?,?,?,?,?,?) """, (None, data['name'], data['number_inst'],
                              data['visit_date'], ratings[data['food_rating']],
                              ratings[data['clean']], data['extra_comments']))



        await state.clear()



    elif message.text == 'n':
        await message.answer('OK')
        await state.clear()
    else:
        await message.answer('"yes" or "no"!')

