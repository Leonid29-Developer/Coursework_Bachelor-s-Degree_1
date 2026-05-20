import tkinter as tk
from tkinter import ttk, filedialog
import csv
import textwrap
import logging

import cypher  # Модуль шифрования


class CSVManagerApp:
    filename = ""
    data = []

    def __init__ (self):
        CSVManagerApp.set_logger()

        self.root = root
        self.root.title("CSV Manager - управление контентом")
        self.root.geometry("800x600")

        # Верхняя панель
        top_frame = tk.Frame(self.root)
        top_frame.place(relwidth = 1, relheight = 0.125)

        # Кнопка - Загрузка Csv
        self.but_load = tk.Button(
                top_frame,
                text = "Загрузить .csv",
                command = self.load_csv)
        self.but_load.place(width = 100, height = 40, x = 20, y = 18)

        # Основная область данных
        table_frame = tk.Frame(
                self.root,
                borderwidth = 0.5,
                relief = 'solid')
        table_frame.place(relwidth = 1, relheight = 0.875, rely = 0.125)

        # Создание таблицы
        columns = ("ID", "Время выгрузки", "IP-адрес", "Расшифрованный текст")
        style = ttk.Style()
        style.configure("Wrap.Treeview", rowheight = 60)
        self.table = ttk.Treeview(
                table_frame,
                show = "headings",
                columns = columns,
                style = "Wrap.Treeview")

        for column in columns:
            self.table.heading(column, text = column)

        self.table.column("ID", width = 60, anchor = "center", stretch = False)
        self.table.column(
                "Время выгрузки",
                width = 140,
                anchor = "center",
                stretch = False)
        self.table.column(
                "IP-адрес",
                width = 120,
                anchor = "center",
                stretch = False)
        self.table.column("Расшифрованный текст", anchor = "w")

        # Полосы прокрутки
        self.scroll_y = tk.Scrollbar(
                table_frame,
                orient = "vertical",
                command = self.table.yview)
        self.table.configure(yscrollcommand = self.scroll_y.set)

        # Размещение элементов
        self.table.place(relwidth = 1, relheight = 1)
        self.scroll_y.pack(side = "right", fill = "y")

    # Настройка логирования
    @staticmethod
    def set_logger ():
        file_handler = logging.FileHandler('logs/manager.log')

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        logger.formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s')
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    # Перенос слов при длине строки более 75 символов
    def wrap (self, string, lenght = 75):
        return '\n'.join(textwrap.wrap(string, lenght))

    # Загрузка файла .csv
    def load_csv (self):
        for item in self.table.get_children():
            self.table.delete(item)

        self.filename = filedialog.askopenfilename(
                title = "Загрузить файл",
                initialdir = "./Data/",  # Начальная директория
                initialfile = "messages.csv",  # Файл по умолчанию
                filetypes = [("Текстовые файлы CSV", "*.csv")])

        with open(self.filename, 'r', encoding = 'utf-8') as file:
            reader = csv.DictReader(file)
            self.data = list(reader)

        for row in self.data:
            self.table.insert(
                    '', 'end', values = (
                            row["id"],
                            row["datetime"],
                            row["ip"],
                            self.wrap(cypher.decrypt(row["text"]))
                            ))


if __name__ == "__main__":
    root = tk.Tk()
    app = CSVManagerApp()
    root.mainloop()
