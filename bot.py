from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from settings import bot_config
from api_requests import request

bot = Bot(token=bot_config.bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class ChoiceCityWeather(StatesGroup):
    waiting_city = State()

@dp.message_handler(commands=['start'])
async def start_message(message):
    markup = types.reply_keyboard.ReplyKeyboardMarkup(row_width=2)
    btn1 = types.KeyboardButton('Погода в моем городе')
    btn2 = types.KeyboardButton('Погода в другом месте')
    btn3 = types.KeyboardButton('История')
    btn4 = types.KeyboardButton('Установить свой город')
    markup.add(btn1, btn2, btn3, btn4)
    text = f'Привет {message.from_user.first_name}, я бот, который расскажет тебе о погоде на сегодня'
    await message.answer(text, reply_markup=markup)
    
@dp.message_handler(regexp='Погода в моем городе')
async def get_user_city_weather(message):
    markup = types.reply_keyboard.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('Меню')
    markup.add(btn1)
    text = 'Я пока не умею'
    await message.answer(text, reply_markup=markup)

@dp.message_handler(regexp='Погода в другом месте')
async def city_start(message: types.Message):
    markup = types.reply_keyboard.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('Меню')
    markup.add(btn1)
    text = 'Введите название города'
    await message.answer(text, reply_markup=markup)
    await ChoiceCityWeather.waiting_city.set()
    
@dp.message_handler(state=ChoiceCityWeather.waiting_city)
async def city_chosen(message: types.Message, state: FSMContext):
    if message.text[0].islower():
        await message.answer('Название города необходимо указывать с большой буквы')
        return
    await state.update_data(waiting_city=message.text)
    markup = types.reply_keyboard.ReplyKeyboardMarkup(row_width=2)
    btn1 = types.KeyboardButton('Погода в моем городе')
    btn2 = types.KeyboardButton('Погода в другом месте')
    btn3 = types.KeyboardButton('История')
    btn4 = types.KeyboardButton('Установить свой город')
    markup.add(btn1, btn2, btn3, btn4)
    city = await state.get_data()
    data = request.get_weather(city.get('waiting_city'))
    text = f'Погода в {city.get("waiting_city")}\nТемпература: {data["temp"]} C\nОщущается как: {data["feels_like"]} C \nСкорость ветра: {data["wind_speed"]}м/с\nДавление: {data["pressure_mm"]}мм'
    await message.answer(text, reply_markup=markup)
    await state.finish()
    
@dp.message_handler(regexp='Меню')
async def start_message(message: types.Message):
    markup = types.reply_keyboard.ReplyKeyboardMarkup(row_width=2)
    btn1 = types.KeyboardButton('Погода в моем городе')
    btn2 = types.KeyboardButton('Погода в другом месте')
    btn3 = types.KeyboardButton('История')
    btn4 = types.KeyboardButton('Установить свой город')
    markup.add(btn1, btn2, btn3, btn4)
    text = f'Привет {message.from_user.first_name}, я бот, который расскажет тебе о погоде на сегодня'
    await message.answer(text, reply_markup=markup)
    

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)