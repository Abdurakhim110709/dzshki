from aiogram import Router, types
from aiogram.filters import Command

start_router = Router()


kb = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [
            types.InlineKeyboardButton(text='Оставить отзыв', callback_data='review')
        ]
    ])
@start_router.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я бот кафе. Чем могу помочь?\n"
                         "наше заведения:/Establishments\n"
                         "Наше меню:/menu\n"
                         "Время работы:/hours\n"
                         "Рандомное блюдо: /random_food", reply_markup=kb)