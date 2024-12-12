from aiogram import Router, types, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

review_router  = Router()

class Review(StatesGroup):
    name = State()
    number_inst = State()
    food_rating = State()
    cleanliness_rating = State()
    extra_comments = State()


@review_router.callback_query(F.data == 'about_as')
async def start_review(call: types.CallbackQuery, state: FSMContext):

    await call.message.answer('Как вас зовут?')
    # await call.message.edit_reply_markup(reply_markup=None)
    await state.set_state(Review.name)

@review_router.message(Review.name)
async def start_review(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Ваш номер или инстаграм')
    await state.set_state(Review.number_inst)

@review_router.message(Review.number_inst)
async def start_review(message: types.Message, state: FSMContext):
    await message.answer('Как оцениваете качества еды')
    await state.update_data(number_inst=message.text)
    await state.set_state(Review.food_rating)


@review_router.message(Review.food_rating)
async def start_review(message: types.Message, state: FSMContext):
    if not message.text.isdigit() or int(message.text) < 1 or int(message.text) > 5:
        await message.answer('Пожалуйста оцените от 1 до 5')
        return
    kb2 = types.InlineKeyboardMarkup(
        inline_keyboard=[

            [
                types.InlineKeyboardButton(text='Чисто', callback_data='about_as_0'),
                types.InlineKeyboardButton(text='Приятненько', callback_data='about_as_1')

            ],
            [

                types.InlineKeyboardButton(text='Грязно', callback_data='about_as_2'),
                types.InlineKeyboardButton(text='Не очень', callback_data='about_as_3')
            ]
        ]
    )
    await message.answer('Как оцениваете чистоту заведения?', reply_markup=kb2)
    await state.update_data(food_rating=message.text)
    await state.set_state(Review.cleanliness_rating)

@review_router.callback_query(F.data.startswith('about_as_'))
async def start_review(call: types.CallbackQuery, state: FSMContext):
    button_data = {
        'about_as_0':'Чисто',
        'about_as_1':'Приятненько',
        'about_as_2':'Грязно',
        'about_as_3':'Не очень'
    }

    await call.message.answer('Дополнительные комментарии/жалоба')
    # await call.message.edit_reply_markup(reply_markup=None)
    await state.update_data(cleanliness_rating=button_data[call.data.lower()])
    await state.set_state(Review.extra_comments)

@review_router.message(Review.extra_comments)
async def start_review(message: types.Message, state: FSMContext):
    await message.answer('Спасибо за отзыв')
    await state.update_data(extra_comments=message.text)
    await state.clear()