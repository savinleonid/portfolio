from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API = "6873090612:AAGSjooC-Sjp89puGsb4eibontNl9X78_k0"
bot = Bot(token=API)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(text=["/start"])
async def start(message: types.Message):
    print("Hi! I am a bot helping with your health.")


@dp.message_handler()
async def all_messages(message: types.Message):
    print("Type the command /start to start conversation.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
