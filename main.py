# Mike_pyb
# import asyncio
import configparser  # библиотека для чтения настроек из других файлов
import pandas as pd  # библиотека для работы с датафреймами

from aiogram import Bot, Dispatcher, types
# from aiogram.types import Message
from aiogram.utils import executor

# читаем настройки
config = configparser.ConfigParser()
config.read('config.ini')
tgkey = config['telegram']['tg_key']

bot = Bot(token=tgkey)
dp = Dispatcher(bot)
tasks_list = ['список дел', 'Список дел', 'tasks', 'Tasks']


@dp.message_handler()
async def send_welcome(message: types.Message):  # Хендлер на любое сообщение
    await message.reply("Я тебя услышал")  # Ответим пользователю шуточным приветствием
    if message.text in tasks_list:  # проверяем полученное сообщение
        await message.answer("вот 2 дела", parse_mode="None")  # отправляем ответное сообщение в чат по id
        excel_list()
        await message.reply(str(printed_tasks), reply=True)
    else:
        await message.answer("Еще не знаком с этой командой. Я понимаю следующие:\n" + str(tasks_list), parse_mode="None")
        # await message.answer("chat_id= " + str(message.chat.id) + " text= " + message.text)

printed_tasks = []  # список задач для печати

# задаем переменные для чтения списка задач
file_path = r'D:\Users\Михаил\YandexDisk\9.Public_Folders\1_GIC\7_Else\gtd_tg.xlsx'  # Указываю полный путь к файлу табл
max_count = 3  # задаю количество задач, которое показать
len_max = 140  # задаю максимальное количество символов для печати из описания задачи


# получаем список задач
def excel_list():
    df = pd.read_excel(file_path)  # читаю файл Excel используя pd.read_excel(**путь или имя**)
    pd.set_option('display.max_rows', None)  # устанавливаю максимальное количество выводимых строк
    pd.set_option('display.max_columns', None)  # устанавливаю максимальное количество выводимых столбцов
    last_row = df.shape[0]  # нахожу последнюю строку
    # last_column = df.shape[1]  # нахожу последний столбец

    # создаю необходимые переменные, имеющие начальное состояние
    categories = []
    count = 0
    # set_tasks = set(range(1, last_row))

    for i in range(1, last_row):
        set_tasks = set(range(1, last_row))
        if max_count - count < last_row - i:
            if df.iloc[i, 3] not in categories:
                count += 1
                categories.append(df.iloc[i, 3])
                # act = df.iloc[i, 4]
                # s_end = ''
                # if len(act) > 140:
                #     s_end = '...'
                # print(
                #     str(count) + '. Тема:', df.iloc[i, 2], '\n',
                #     'Категория:', df.iloc[i, 3],
                #     'Действия:\n' + act[:140] + s_end
                # )
                printed_tasks.append(i)
        else:
            count += 1
            num_task = list(set_tasks.difference(set(printed_tasks)))
            num_task = sorted(num_task)

            # act = df.iloc[i, 4]
            # s_end = ''
            # if len(act) > 140:
            #     s_end = '...'
            # print(num_task, type(num_task))
            # print(num_task[0])
            # print(
            #     str(count) + '. Тема', df.iloc[num_task[0], 2], '\n',
            #     'Категория:', df.iloc[num_task[0], 3],
            #     'Действия:\n' + act[:140] + s_end
            # )
            printed_tasks.append(num_task[0])  # добавляем напечатанную задачу
            # print(printed_tasks)
        if count == max_count:
            break
    return printed_tasks


if __name__ == '__main__':  # конструкция для запуска бота
    executor.start_polling(dp, skip_updates=True)
    
