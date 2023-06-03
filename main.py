# Mike_pyb
import configparser  # библиотека для чтения настроек из других файлов
import pandas as pd  # библиотека для работы с датафреймами

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# читаем настройки из файла
config = configparser.ConfigParser()
config.read('config.ini')
tgkey = config['telegram']['tg_key']

# создаем тг бота
bot = Bot(token=tgkey)
dp = Dispatcher(bot)

# задаем списки
tasks_list = ['список дел', 'список задач', 'tasks', 'актуальное', 'actual', 'задачи']  # запросы для вызова списка дел
morning_list = ['Доброе утро', 'утро', 'доброе', 'morning']  # команды для начала дня


# обрабатываем команду /morning
@dp.message_handler(commands=morning_list)
async def send_greeting(message: types.Message):
    await message.reply('Доброе утро!')  # отправляем сообщение "доброе утро" в ответ на команду


# обрабатываем команду /tasks
@dp.message_handler(commands='tasks')
async def send_greeting(message: types.Message):
    await message.reply('Кое-что есть!\nВот список актуальных задач:',
                        reply=True)  # отправляем сообщение "доброе утро" в ответ на команду
    excel_list = excel_list_def()
    tasks4print = print_tasks_list(excel_list)
    for i in range(0, len(tasks4print)):
        await message.answer(tasks4print[i])


# Хенд лер на любое сообщение
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
    else:
        await message.answer(
            "Еще не знаком с этими словами. Я понимаю следующие слова:\n" + str(tasks_list), parse_mode="None")


printed_tasks = []  # список задач для печати

# задаем переменные для чтения списка задач
file_path = r'D:\Users\Михаил\YandexDisk\9.Public_Folders\1_GIC\7_Else\gtd_tg.xlsx'  # Указываю полный путь к файлу табл
max_count = 3  # задаю количество задач, которое показать
max_len = 140  # задаю максимальное количество символов для печати из описания задачи

# создаю датафрейм и настраиваю
df = pd.read_excel(file_path)  # читаю файл Excel используя pd.read_excel(**путь или имя**)
pd.set_option('display.max_rows', None)  # устанавливаю максимальное количество выводимых строк
pd.set_option('display.max_columns', None)  # устанавливаю максимальное количество выводимых столбцов
last_row = df.shape[0]  # нахожу последнюю строку


# last_column = df.shape[1]  # нахожу последний столбец


# получаем список актуальных задач
def excel_list_def():
    # создаю необходимые переменные, имеющие начальное состояние
    categories = []
    count = 0

    for i in range(1, last_row):
        set_tasks = set(range(1, last_row))
        if max_count - count < last_row - i:
            if df.iloc[i, 3] not in categories:
                count += 1
                categories.append(df.iloc[i, 3])
                printed_tasks.append(i)
                # печать параметров внутри цикле
                # print('count=', count, 'i=', i, 'df.iloc[i,3]=', df.iloc[i, 3], 'categories=', categories,
                # 'last_row=', last_row, '\n', 'printed_tasks=', printed_tasks, )
        else:
            count += 1
            num_task = list(set_tasks.difference(set(printed_tasks)))
            num_task = sorted(num_task)
            printed_tasks.append(num_task[0])  # добавляем напечатанную задачу
            # печать параметров внутри цикле
            # print('count=', count, 'i=', i, 'df.iloc[i,3]=', df.iloc[i, 3], 'categories=', categories, 'last_row=',
            #       last_row, '\n', 'printed_tasks=', printed_tasks, )
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
