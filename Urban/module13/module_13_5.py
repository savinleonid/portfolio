from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

API = ""
bot = Bot(token=API)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
calc_button = KeyboardButton(text="Calculate")
info_button = KeyboardButton(text="Info")
kb.insert(calc_button)
kb.insert(info_button)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text=["Calculate"])
async def set_age(message: types.Message):
    await message.answer("Enter your age.")
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state):
    await state.update_data(age=message.text)
    await message.answer("Enter your height.")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state):
    await state.update_data(growth=message.text)
    await message.answer("Enter your weight.")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def set_weight(message: types.Message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    norm_calories = 10 * float(data["weight"]) + 6.25 * float(data["growth"]) - 5 * int(data["age"]) + 5  # for men
    await message.answer(f"Your calorie norm is {norm_calories:.2f}")
    await state.finish()


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Hi! I am a bot helping with your health.", reply_markup=kb)


@dp.message_handler()
async def all_messages(message: types.Message):
    await message.answer("Type command /start to start conversation.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
