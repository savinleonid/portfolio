from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from crud_functions import *


API = ""
bot = Bot(token=API)
dp = Dispatcher(bot, storage=MemoryStorage())

initiate_db()
products = get_all_products()

kb = ReplyKeyboardMarkup(resize_keyboard=True)
calc_button = KeyboardButton(text="Calculate")
info_button = KeyboardButton(text="Info")
buy_button = KeyboardButton(text="Buy")
registration_button = KeyboardButton(text="Registration")
kb.insert(calc_button)
kb.insert(info_button)
kb.add(buy_button)
kb.add(registration_button)

inline_kb = InlineKeyboardMarkup()
inline_buy_kb = InlineKeyboardMarkup()
calc_norm_btn = InlineKeyboardButton(text="Calculate Norm", callback_data="calories")
formula_btn = InlineKeyboardButton(text="Formula", callback_data="formulas")
product1_btn = InlineKeyboardButton(text="Product 1", callback_data="product_buying")
product2_btn = InlineKeyboardButton(text="Product 2", callback_data="product_buying")
product3_btn = InlineKeyboardButton(text="Product 3", callback_data="product_buying")
product4_btn = InlineKeyboardButton(text="Product 4", callback_data="product_buying")
inline_kb.add(calc_norm_btn, formula_btn)
inline_buy_kb.row(product1_btn, product2_btn, product3_btn, product4_btn)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State("1000")  # not needed, adding by default in add_user crud function


@dp.message_handler(text="Registration")
async def sing_up(message: types.Message):
    await message.answer("Enter username (Latin alphabet only):")
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message: types.Message, state):
    if not is_included(message.text):
        await state.update_data(username=message.text)
        await message.answer("Enter your email:")
        await RegistrationState.email.set()
    else:
        await message.answer("User exists, please enter another username")
        await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message: types.Message, state):
    await state.update_data(email=message.text)
    await message.answer("Enter your age:")
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    user = await state.get_data()
    add_user(user["username"], user["email"], user["age"])
    await message.answer("Registered successfully!")
    await state.finish()


@dp.message_handler(text="Calculate")
async def main_menu(message: types.Message):
    await message.answer("Choose option:", reply_markup=inline_kb)


@dp.message_handler(text="Buy")
async def get_buying_list(message: types.Message):
    for product in get_all_products():
        await message.answer(f"Name: {product[1]} | Description: {product[2]} | Price: {product[3]}")
        with open(f"pics/prod{product[0]}.png", "rb") as img:
            await message.answer_photo(img)
    await message.answer("Choose product to buy:", reply_markup=inline_buy_kb)


@dp.callback_query_handler(text="formulas")
async def get_formulas(call: types.CallbackQuery):
    await call.message.answer("10 x weight(kg) + 6.25 x height(cm) - 5 x age(y) + 5")
    await call.answer()


@dp.callback_query_handler(text="calories")
async def set_age(call: types.CallbackQuery):
    await call.message.answer("Enter your age.")
    await UserState.age.set()
    await call.answer()


@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call: types.CallbackQuery):
    await call.message.answer("Purchase succeeded!")
    await call.answer()


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
    connection.close()
