import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
import logging
import os
import textwrap
import time
import tkinter as tk
import urllib.parse
from datetime import datetime
from http.client import HTTPConnection as Connection
from tkinter import ttk, filedialog, messagebox

from cypher import decrypt  # Модуль шифрования


# Ошибка - Чтение файла не CSV
class FileReadingNotCSV(Exception):
    def __init__ (self):
        super().__init__("Файл должен иметь формат .csv")


# Ошибка - Не удалось отправить сообщение при отправке на сервер
class SendServerError(Exception):
    def __init__ (self):
        super().__init__("Не удалось отправить сообщение")


class CSVManagerApp:
    filename = ""
    data = []
    logger = logging.getLogger(__name__)
    open_win = False
    button_frame_active = {'bool': False, 'row_id': 0}

    def __init__ (self):
        self.set_logger()

        self.root = root
        self.root.title("CSV Manager - управление контентом")
        self.root.geometry("800x600")

        # Главная форма
        self._main_form()

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
                logging.Formatter(
                        '[%(asctime)s] - [%(levelname)s] - %(message)s'))

        # Обработчик для консоли: WARNING и выше
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(
                logging.Formatter('[%(levelname)s] - %(message)s'))

        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    # Инициализация главной формы
    def _main_form (self):
        # Верхняя панель
        top_frame = tk.Frame(self.root)
        top_frame.place(relwidth = 1, relheight = 0.125)

        # Кнопка - Загрузка Csv
        but_load = tk.Button(
                top_frame,
                text = "Загрузить .csv",
                command = self.load_csv, background = "#B4D1D5")
        but_load.place(width = 100, height = 40, x = 30, y = 18)

        # Кнопка - Создать Csv
        but_create = tk.Button(
                top_frame,
                text = "Создать .csv",
                command = self.create_csv, background = "#B4D1D5")
        but_create.place(width = 100, height = 40, x = 160, y = 18)

        # Кнопка - Добавить новую строку
        but_new_line = tk.Button(
                top_frame,
                text = "Добавить новую строку",
                command = self._add_new_line, background = "#B4D1D5")
        but_new_line.place(width = 150, height = 40, x = 290, y = 18)

        # Основная область данных
        self.table_frame = tk.Frame(
                self.root,
                borderwidth = 0.5,
                relief = 'solid')
        self.table_frame.place(relwidth = 1, relheight = 0.875, rely = 0.125)

        # Создание таблицы
        columns = (
                "0", "ID", "Время выгрузки", "IP-адрес",
                "Расшифрованный текст")
        style = ttk.Style()
        style.configure("Wrap.Treeview", rowheight = 60)
        self.table = ttk.Treeview(
                self.table_frame,
                show = "headings",
                columns = columns,
                style = "Wrap.Treeview")

        for column in columns:
            if column != "0":
                self.table.heading(column, text = column)

        self.table.column("0", width = 70, anchor = "center", stretch = False)
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
                self.table_frame,
                orient = "vertical",
                command = self.table.yview)
        self.table.configure(yscrollcommand = self.scroll_y.set)

        # Размещение элементов
        self.table.place(relwidth = 1, relheight = 1)
        self.scroll_y.pack(side = "right", fill = "y")

        # События для побочных кнопок строк
        self.table.bind('<Motion>', self.yes_mouse_detect)
        self.table.bind('<Leave>', self.no_mouse_detect)

    # Событие - перемещение мыши в области таблицы
    def yes_mouse_detect (self, event):
        row_id = self.table.identify_row(event.y)
        if row_id and self.button_frame_active['row_id'] != row_id:
            self.no_mouse_detect(event)
            self._create_button(row_id)

    # Инициализация кнопок для строк
    def _create_button (self, row_id):
        bbox = self.table.bbox(row_id, 0)

        if bbox:
            x, y, width, height = bbox

            self.button_frame = tk.Frame(self.table, name = f"frame_{row_id}")

            but_up = tk.Button(
                    self.button_frame,
                    text = "↑",
                    width = 2,
                    font = ("Segoe UI", 10),
                    command = lambda deviation = -1: self.edit_and_save_csv(
                            deviation))
            but_down = tk.Button(
                    self.button_frame,
                    text = "↓",
                    width = 2,
                    font = ("Segoe UI", 10),
                    command = lambda deviation = 1: self.edit_and_save_csv(
                            deviation))
            but_del = tk.Button(
                    self.button_frame,
                    text = "×",
                    width = 2,
                    font = ("Segoe UI", 10),
                    foreground = "red",
                    command = lambda deviation = 0: self.edit_and_save_csv(
                            deviation))
            but_up.pack(side = "left")
            but_down.pack(side = "left")
            but_del.pack(side = "left")
            self.button_frame_active['bool'] = True
            self.button_frame_active['row_id'] = row_id
            self.button_frame.place(x = 0, y = y, height = height)

            # Активация / Деактивация кнопок, в зависимости от расположения
            index = self.table.index(row_id)
            count = len(self.table.get_children())

            if index == 0:
                but_up.configure(state = "disabled", background = "#A0A0A0")
            if index == count - 1:
                but_down.configure(state = "disabled", background = "#A0A0A0")

    # Событие - выход мыши из области таблицы
    def no_mouse_detect (self, event = None):
        row_id = self.table.identify_row(event.y)
        if self.button_frame_active['row_id'] != row_id:
            if self.button_frame_active['bool']:
                self.button_frame.destroy()
                self.button_frame_active = {'bool': False, 'row_id': 0}

    # Изменение порядка строк и сохранение новых данных в файл csv
    def edit_and_save_csv (self, deviation):
        row_id = self.button_frame_active['row_id']
        index = self.table.index(row_id)
        values = self.table.item(row_id)['values']

        # Обновить в таблице
        self.table.delete(row_id)
        if deviation != 0:
            self.table.insert(
                    '', index + deviation, iid = row_id, values = (
                            "",
                            values[1],  # id
                            values[2],  # datetime
                            values[3],  # ip
                            values[4],  # text
                            ))

        # Обновление в словаре данных
        data_id = [item['id'] for item in self.data]
        index = data_id.index(str(values[1]))
        value = self.data[index]
        self.data.remove(value)
        if deviation != 0:
            self.data.insert(index + deviation, value)

        # Обновление в файле csv
        with (open(self.filename, 'w', encoding = 'utf-8') as file):
            file.write("datetime,id,ip,text\n")
            for item in self.data:
                file.write(
                        f"{item['datetime']},{item['id']},{item['ip']},{item['text']}\n")

    # Перенос слов при длине строки более 75 символов
    # noinspection PyBroadException
    def wrap (self, string, lenght = 75):
        return '\n'.join(textwrap.wrap(string, lenght))

    # Загрузка файла .csv
    def load_csv (self):
        try:
            # Подтверждение перезаписи данных
            if len(self.data) > 0:
                if not messagebox.askyesno(
                        "Подтверждение",
                        "Загрузить новый CSV-файл? Существующие данные будут перезаписаны."):
                    return

            for item in self.table.get_children():
                self.table.delete(item)

            self.filename = filedialog.askopenfilename(
                    title = "Загрузить файл",
                    initialdir = "./Data/",  # Начальная директория
                    initialfile = "messages.csv",  # Файл по умолчанию
                    filetypes = [("Текстовые файлы CSV", "*.csv")])

            # Выйти если путь пуст
            if self.filename == "": return

            # Проверка формата файла
            if os.path.splitext(self.filename)[1] == ".csv":
                self.logger.info(f"[Прочитан файл csv] - {self.filename}")
            else:
                raise FileReadingNotCSV()

            with open(self.filename, 'r', encoding = 'utf-8') as file:
                reader = csv.DictReader(file)
                self.data = list(reader)

            error_index = False

            for row in self.data:
                text_decrypt = decrypt(row["text"])

                # Проверка строк на корректность
                if text_decrypt == "er0":
                    error_index = True
                else:
                    self.table.insert(
                            '', 'end', values = (
                                    "",
                                    row["id"],
                                    row["datetime"],
                                    row["ip"],
                                    self.wrap(text_decrypt)
                                    ))

            if error_index:
                self.logger.warning(
                        f"[Ошибка чтения файла] - Не удалось прочитать некоторые данные")
                messagebox.showwarning(
                        "Ошибка чтения файла",
                        "Не удалось прочитать некоторые данные")

        except FileReadingNotCSV as error:
            self.logger.error(f"[Ошибка чтения файла] - {self.filename}")
            messagebox.showerror("Ошибка чтения файла", str(error))

        except KeyError:
            self.logger.error(
                    f"[Ошибка чтения файла] - Структура файла не соответствует требуемым")
            messagebox.showerror(
                    "Ошибка чтения файла",
                    "Структура файла не соответствует требуемым")

    # Создание и выбор места для сохранения файла
    def create_csv (self):
        # Подтверждение перезаписи данных
        if len(self.data) > 0:
            if not messagebox.askyesno(
                    "Подтверждение",
                    "Создать новый CSV-файл? Существующие данные будут перезаписаны."):
                return

        for item in self.table.get_children():
            self.table.delete(item)
        self.data = []

        # Вызов диалогового окна сохранения
        self.filename = filedialog.asksaveasfilename(
                title = "Сохранить файл",
                filetypes = [
                        ("Текстовые файлы CSV", "*.csv")
                        ],
                initialfile = "messages.csv",  # Файл по умолчанию
                defaultextension = ".csv"
                )

    # Запуск процедуры добавления новой строки
    def _add_new_line (self):
        if self.filename == "":
            self.create_csv()  # Выбор места сохранения при не выбранном файле
            if self.filename == "": return  # Выход, если файл так и не выбран

        # Создание окна-ввода
        if not self.open_win:
            self.input_win = tk.Toplevel(self.root)
            self.input_win.geometry(
                    f"400x250+{root.winfo_x() + 260}+{root.winfo_y() + 180}")

            self.input_win.bind('<Destroy>', self.destroy_input_win)

            win_frame = tk.Frame(self.input_win)
            win_frame.place(relwidth = 1, relheight = 1)

            label_title = tk.Label(
                    win_frame,
                    text = "Введите текст для новой строки",
                    font = ("Segoe UI", 11))
            label_title.place(
                    relwidth = 0.8,
                    relheight = 0.1,
                    relx = 0.1,
                    rely = 0.05)

            self.input_textbox = tk.Text(
                    win_frame,
                    borderwidth = 0.5,
                    relief = 'solid')
            self.input_textbox.bind('<Return>', self.entry_send_content)
            self.input_textbox.place(
                    relwidth = 0.8,
                    relheight = 0.6,
                    relx = 0.1,
                    rely = 0.2)

            button_send = tk.Button(
                    win_frame,
                    text = "Отправить",
                    borderwidth = 0.5,
                    relief = 'solid',
                    font = ("Segoe UI", 11),
                    background = "#B4D1D5",
                    command = self.send_content)
            button_send.place(
                    relwidth = 0.4,
                    relheight = 0.1,
                    relx = 0.3,
                    rely = 0.85)

            self.open_win = True

    # Событие - выход или закрытие окна
    def destroy_input_win (self, event):
        self.open_win = False

    # Событие - нажатие <Enter> в textbox в форме input
    def entry_send_content (self, event):
        self.send_content()

    # Добавление новой строки через сервер в файл и в таблицу для визуализации
    def send_content (self):
        try:
            # Добавление новой строки через сервер в файл
            data_load = urllib.parse.urlencode(
                    {
                            "ip": "admin",
                            "text": self.input_textbox.get("1.0", "end-1c"),
                            "filename": self.filename})
            connect = Connection('127.0.0.1', 5000)
            connect.request(
                    "POST",
                    "/hidden/",
                    data_load,
                    {'Content-type': 'application/x-www-form-urlencoded'})
            if connect.getresponse().status == 200:
                self.logger.info("[Сообщение успешно отправлено]")
            else: raise SendServerError

            fix_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # Остановка работы приложения на время работы сервера
            time.sleep(0.0006)
            with open(self.filename, 'r', encoding = 'utf-8') as file:
                reader = csv.DictReader(file)
                for row in list(reader):
                    if fix_datetime == row["datetime"]:
                        self.table.insert(
                                '', 'end', values = (
                                        "",
                                        row["id"],
                                        row["datetime"],
                                        row["ip"],
                                        self.wrap(decrypt(row["text"]))
                                        ))
                        self.data.append(row)
            self.table.see(self.table.get_children()[-1])

            self.input_win.destroy()

        except SendServerError as error:
            self.logger.error(f"[Ошибка при отправке сообщения]")
            messagebox.showerror("Ошибка", str(error))


if __name__ == "__main__":
    root = tk.Tk()
    app = CSVManagerApp()
    root.mainloop()
