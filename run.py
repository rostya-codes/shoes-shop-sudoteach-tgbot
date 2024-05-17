import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from icecream import ic

from app.admin import admin as admin_router
from app.database.models import async_main
from app.handlers import router as user_router


async def main():
    """Main function returns coroutine"""
    load_dotenv()

    await async_main()

    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()

    dp.include_routers(
        user_router,
        admin_router
    )

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        ic('Bot is OFF!')
