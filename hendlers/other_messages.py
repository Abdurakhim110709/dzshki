from aiogram import Router, types

echo_router = Router()


@echo_router.message()
async def echo_hendler(message: types.Message):
    txt = message.text
    # await message.answer(txt)
    await message.bot.send_message(
        chat_id=message.from_user.id,
        text="Я вас не понимаю!"
    )
