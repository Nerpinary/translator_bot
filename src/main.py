from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from src.config import BOT_TOKEN
from src.handlers import common, text

async def main():
    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)
    
    common.register_handlers(dp)
    text.register_handlers(dp)
    
    await dp.start_polling()

if __name__ == '__main__':
    main()