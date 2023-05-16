# Mike_pyb
import asyncio
import configparser

from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor

config = configparser.ConfigParser()
config.read('config.ini')
tgkey = config['telegram']['tg_key']

bot = Bot(token=tgkey)
dp = Dispatcher(bot)


@dp.message_handler()
async def send_welcome(message: types.Message): # Хендлер на любое сообщение
    await message.reply("Привет, медвед!") # Ответим пользователю шуточным приветствием


if __name__ == '__main__': # конструция для запуска бота
    executor.start_polling(dp, skip_updates=True)
    