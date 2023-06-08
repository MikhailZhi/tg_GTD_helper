# Mike_pyb
import configparser  # библиотека для чтения настроек из других файлов
import pandas as pd  # библиотека для работы с датафреймами
# import openpyxl

from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
from datetime import datetime

file_path = r'D:\Users\Михаил\gdrive_off\GIC\Helper\gtd_tg.xlsx'  # Указываю полный путь к файлу таблицы

# читаем настройки из файла
config = configparser.ConfigParser()
config.read('config.ini')
tg_key = config['telegram']['tg_key']

# создаем тг бота
bot = Bot(token=tg_key)
dp = Dispatcher(bot)

# задаем списки
tasks_list = ['список дел', 'список задач', 'tasks', 'актуальное', 'actual', 'задачи']  # запросы для вызова списка дел
morning_list = ['доброе утро', 'утро', 'доброе', 'morning']  # команды для начала дня


# обрабатываем команду /morning
@dp.message_handler(commands='morning')
async def send_morning(message: types.Message):
    # Создаем кнопки
    button_wakeup = InlineKeyboardButton(text="Проснулся", callback_data="wakeup")
    button_getup = InlineKeyboardButton(text="Встал", callback_data="getup")
    button_fresh = InlineKeyboardButton(text="Умылся", callback_data="fresh")
    button_breakfast_cooked = InlineKeyboardButton(text="Приготовил завтрак", callback_data="breakfast_cooked")
    button_breakfast_finished = InlineKeyboardButton(text="Позавтракал", callback_data="breakfast_finished")

    # Создаем объект клавиатуры и добавляем кнопки в одну строку
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(button_wakeup, button_getup, button_fresh, button_breakfast_cooked, button_breakfast_finished)

    await message.reply('Доброе утро!', reply=True, reply_markup=markup)  # Отправка сообщения с кнопками


# реагируем на кнопочки
@dp.callback_query_handler(lambda callback_query: 'wakeup' in callback_query.data)
async def morning_timers(callback_query: types.CallbackQuery):
    if callback_query.data == "wakeup":
        time_wakeup = datetime.now()
        await bot.send_message(chat_id=callback_query.message.chat.id, text=f"Goal! \n {time_wakeup}")


async def morning_cell():
    pass


# обрабатываем команду /tasks
@dp.message_handler(commands='tasks')
async def send_tasks(message: types.Message):
    await message.reply('Кое-что есть!\nВот список актуальных задач:', reply=True)  # отправляем список задач
    excel_list = excel_list_def()
    tasks4print = print_tasks_list(excel_list)
    for i in range(0, len(tasks4print)):
        await message.answer(tasks4print[i])


# Обрабатываем любое текстовое сообщение
@dp.message_handler(content_types=types.ContentType.TEXT)
async def any_message(message: types.Message):
    await message.reply("Я тебя услышал!")  # Ответим пользователю шуточным приветствием
    if message.text.lower() in tasks_list:  # проверяем полученное сообщение
        # await message.answer("вот 2 дела", parse_mode="None")  # отправляем ответное сообщение в чат по id
        excel_list = excel_list_def()
        # await message.answer(str(excel_list))
        tasks4print = print_tasks_list(excel_list)
        for i in range(0, len(tasks4print)):
            await message.answer(tasks4print[i])
        # await message.reply(str(printed_tasks), reply=True)
    elif message.text.lower() in morning_list:
        await send_morning()
    else:
        await message.answer(
            "Еще не знаком с этими словами. Я понимаю следующие слова:\n" + str(tasks_list), parse_mode="None")


printed_tasks = []  # список задач для печати

# задаем переменные для чтения списка задач
max_count = 3  # задаю количество задач, которое показать
max_len = 140  # задаю максимальное количество символов для печати из описания задачи

# создаю датафрейм и настраиваю
df = pd.read_excel(file_path)  # читаю файл Excel используя pd.read_excel(**путь или имя**)
pd.set_option('display.max_rows', None)  # устанавливаю максимальное количество выводимых строк
pd.set_option('display.max_columns', None)  # устанавливаю максимальное количество выводимых столбцов
last_df_row = df.shape[0]  # нахожу последнюю строку; last_column = df.shape[1]  # нахожу последний столбец


# получаем список актуальных задач
def excel_list_def():
    # создаю необходимые переменные, имеющие начальное состояние
    categories = []
    count = 0
    for i in range(1, last_df_row):
        set_tasks = set(range(1, last_df_row))
        if max_count - count < last_df_row - i:
            if df.iloc[i, 3] not in categories:
                count += 1
                categories.append(df.iloc[i, 3])
                printed_tasks.append(i)
        else:
            count += 1
            num_task = list(set_tasks.difference(set(printed_tasks)))
            num_task = sorted(num_task)
            printed_tasks.append(num_task[0])  # добавляем напечатанную задачу
        if count == max_count:
            break
    return printed_tasks


# собираю список с текстами задач для печати
def print_tasks_list(excel_list: list):
    printed = []
    for i in range(1, len(excel_list) + 1):
        act = str(df.iloc[i, 4])
        s_end = ''
        if len(act) > max_len:
            s_end = '...'
        printed.append(
            str(i) + '. Тема: ' + str(df.iloc[i, 2]) + '\n' + 'Категория: ' +
            str(df.iloc[i, 3]) + '\n' + 'Действия: \n' + act[:max_len] + s_end
        )
    return printed


if __name__ == '__main__':  # конструкция для запуска бота
    executor.start_polling(dp, skip_updates=True)
