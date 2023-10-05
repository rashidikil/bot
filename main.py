from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from database import add_new_user, connect_to_db
from database import get_task
from geopy.distance import geodesic
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "6123011746:AAEE3x-kx8RaP72D_SgrlEcaNZBA17TpTOM"

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

class Registration(StatesGroup):
    waiting_for_username = State()

@dp.message_handler(commands='start', state='*')
async def cmd_start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Регистрация")
    await message.answer("Добро пожаловать! Нажмите на 'Регистрация' для начала.", reply_markup=markup)
    await Registration.waiting_for_username.set()

@dp.message_handler(state=Registration.waiting_for_username, content_types=types.ContentTypes.TEXT)
async def process_username(message: types.Message, state: FSMContext):
    username = message.text
    # Здесь должна быть проверка на уникальность username
    add_new_user(username, message.from_user.id)
    await state.finish()

async def give_task(user_id, task_id):
    task = get_task(task_id)
    await bot.send_message(user_id, task['text'])

# Добавьте новую переменную состояния для хранения текущего задания
class TaskHandler(StatesGroup):
    waiting_for_answer = State()

# Функция give_task теперь устанавливает состояние ожидания ответа
async def give_task(user_id, task_id):
    task = get_task(task_id)
    await bot.send_message(user_id, task['text'])
    await TaskHandler.waiting_for_answer.set()

@dp.message_handler(state=TaskHandler.waiting_for_answer, content_types=types.ContentTypes.TEXT)
async def process_answer(message: types.Message, state: FSMContext):
    user_answer = message.text
    # Здесь проверка правильности ответа, для этого нужно будет использовать функцию из database.py

    await state.finish()

@dp.message_handler(content_types=types.ContentTypes.LOCATION)
async def process_location(message: types.Message):
    user_location = message.location
    latitude = user_location.latitude
    longitude = user_location.longitude
    # Здесь логика проверки геолокации

@dp.message_handler(content_types=types.ContentTypes.LOCATION)
async def process_location(message: types.Message):
    user_location = message.location
    latitude = user_location.latitude
    longitude = user_location.longitude

    # предположим, target_location это координаты цели, которые вы ранее отправили пользователю
    target_location = (target_latitude, target_longitude)
    current_location = (latitude, longitude)

    distance = geodesic(target_location, current_location).meters

    if distance <= 10:
        # Пользователь находится в пределах окружности
        await bot.send_message(message.chat.id, "Вы на месте!")
    else:
        # Пользователь вне окружности
        await bot.send_message(message.chat.id, "Вы не на месте, двигайтесь к цели.")

# Создание клавиатуры
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton("Получить другое задание")
keyboard.add(button)

async def give_task(user_id, task_id):
    task = get_task(task_id)
    await bot.send_message(user_id, task['text'], reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "Получить другое задание")
async def get_another_task(message: types.Message):
# Логика для получения другого задания

executor.start_polling(dp, skip_updates=True)
