import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from database.db import init_db
from handlers.user.menu import setup_user_menu
from handlers.user.cart import setup_cart_handlers
from handlers.user.checkout import setup_checkout_handlers
from handlers.admin.products import setup_product_handlers
from handlers.admin.settings import setup_settings_handlers

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

async def main():
    init_db()
    
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    
    setup_user_menu(dp)
    setup_cart_handlers(dp)
    setup_checkout_handlers(dp)
    setup_product_handlers(dp)
    setup_settings_handlers(dp)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
