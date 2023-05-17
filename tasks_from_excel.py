import pandas as pd

file_path = r'D:\Users\Михаил\YandexDisk\9.Public_Folders\1_GIC\7_Else\gtd_tg.xlsx'  # Указываю полный путь к файлу табл
max_tasks = 3
max_len = 140

df = pd.read_excel(file_path)
pd.set_option('display.max_rows', None)  # устанавливаю максимальное количество выводимых строк
pd.set_option('display.max_columns', None)  # устанавливаю максимальное количество выводимых столбцов
last_row = df.shape[0]  # нахожу последнюю строку

tasks_list = []
counter = 0


def def_tasks_list():
    for i in range(1, last_row):
        print(df.iloc[i, 3])
    pass


if __name__ == '__main__':
    def_tasks_list()
