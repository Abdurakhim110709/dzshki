import asyncio
import logging
from bot_config import dp, bot, db
from hendlers.hours import hours_router
from hendlers.menu import menu_router
from hendlers.my_info import myinfo
from hendlers.other_messages import echo_router
from hendlers.picture import picture
from hendlers.random_command import random_us
from hendlers.start import start_router
from hendlers.review import review_router
from hendlers.add_dish import add_dish_router
from hendlers.get_dish import get_dihs_router


async def on_startup():
    database.create_tablse()


async def main():
    db.create_tables()
    dp.include_router(hours_router)
    dp.include_router(menu_router)
    dp.include_router(add_dish_router)
    dp.include_router(get_dihs_router)
    dp.include_router(start_router)
    dp.include_router(picture)
    dp.include_router(myinfo)
    dp.include_router(review_router)
    dp.include_router(random_us)
    dp.include_router(echo_router)


    # Запуск бота
    await dp.start_polling(bot), on_startup()


if __name__ == '__main__':
    asyncio.run(main())
    logging.basicConfig(level=logging.INFO)

