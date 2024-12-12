import asyncio
from bot_config import dp, bot
from hendlers.hours import hours_router
from hendlers.menu import menu_router
from hendlers.my_info import myinfo
from hendlers.other_messages import echo_router
from hendlers.picture import picture
from hendlers.random_command import random_us
from hendlers.start import start_router
from hendlers.review import review_router


async def main():
    dp.include_router(hours_router)
    dp.include_router(menu_router)
    dp.include_router(start_router)
    dp.include_router(picture)
    dp.include_router(myinfo)
    dp.include_router(random_us)
    dp.include_router(review_router)
    dp.include_router(echo_router)
    #Запуск бота
    await dp.start_polling(bot)
if __name__ == '__main__':
   asyncio.run(main())
