from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API = ""
bot = Bot(token=API)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(text=["/start"])
async def start(message: types.Message):
    await message.answer("Hi! I am a bot helping with your health.")


@dp.message_handler()
async def all_messages(message: types.Message):
    await message.answer("Type command /start to start conversation.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
