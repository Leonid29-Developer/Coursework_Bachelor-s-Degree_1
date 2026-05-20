import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
import textwrap
import logging
import os
import cypher  # Модуль шифрования


# Ошибка - Чтение файла не CSV
class FileReadingNotCSV(Exception):
    def __init__ (self):
        super().__init__("Файл должен иметь формат .csv")


class CSVManagerApp:
    filename = ""
    data = []
    logger = logging.getLogger(__name__)

    def __init__ (self):
        self.set_logger()

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
    def set_logger (self):
        # Повторное создание папки для логов, если удалена
        os.makedirs('logs', exist_ok = True)

        # Обработчик для файла: DEBUG и выше
        file_handler = logging.FileHandler(
                'logs/manager.log',
                encoding = 'utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(
                logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

        # Обработчик для консоли: WARNING и выше
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(
                logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    # Перенос слов при длине строки более 75 символов
    def wrap (self, string, lenght = 75):
        return '\n'.join(textwrap.wrap(string, lenght))

    # Загрузка файла .csv
    def load_csv (self):
        try:
            for item in self.table.get_children():
                self.table.delete(item)

            self.filename = filedialog.askopenfilename(
                    title = "Загрузить файл",
                    initialdir = "./Data/",  # Начальная директория
                    initialfile = "messages.csv",  # Файл по умолчанию
                    filetypes = [("Текстовые файлы CSV", "*.csv")])

            if os.path.splitext(self.filename)[1] == ".csv":
                self.logger.info(f"[Прочитан файл csv] - {self.filename}")
            else:
                raise FileReadingNotCSV()

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

        except FileReadingNotCSV as error:
            self.logger.error(f"[Ошибка чтения файла] - {self.filename}")
            messagebox.showerror("Ошибка чтения файла", str(error))


if __name__ == "__main__":
    root = tk.Tk()
    app = CSVManagerApp()
    root.mainloop()
