from aiogram import Router, F, types
from aiogram.filters import Command

start_router = Router()
@start_router.message(Command('start'))
async def cmd_start(message: types.Message):
     kb = types.InlineKeyboardMarkup(
         inline_keyboard=[

                [
                    types.InlineKeyboardButton(text='Оставить отзыв', callback_data='about_as')
                ]
         ]
     )
     await message.answer("Привет! Я бот кафе. Чем могу помочь?\n"
                          "наше заведения:/Establishments\n"
                          "Наше меню:/menu\n"
                          "Время работы:/hours\n"
                          "Рандомное блюдо: /random_food", reply_markup=kb)


