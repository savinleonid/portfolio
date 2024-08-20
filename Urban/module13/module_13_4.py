from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

API = ""
bot = Bot(token=API)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text=["Calories"])
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


@dp.message_handler(text=["/start"])
async def start(message: types.Message):
    await message.answer("Hi! I am a bot helping with your health.")


@dp.message_handler()
async def all_messages(message: types.Message):
    await message.answer("Type command /start to start conversation.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
