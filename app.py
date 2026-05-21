import tkinter as tk
from tkinter import (filedialog, scrolledtext as scroll_text)
import cypher  # Модуль шифрования


# Ошибка: Файл содержит недопустимые символы в строке
class FileInvalidCharacters(Exception):
    def __init__ (self, index_line):
        message = f"Файл содержит недопустимые символы на строке №{index_line}"
        super().__init__(message)


class EncryptionWindow:
    ID = "70220069"  # ID студента
    length_content = ""  # Количество отображаемых строк для данных из файла
    # Количество отображаемых строк для добавления в файл
    length_add = 3 + int(ID) % 4
    data_lines = ""  # Обрабатываемые данные (текст)

    # Открывает диалоговое окно выбора файла
    def file_load (self):
        filename = filedialog.askopenfilename(
                title = "Загрузить файл",
                initialdir = "./Data/",  # Начальная директория
                initialfile = "encrypt.txt",  # Файл по умолчанию
                filetypes = [
                        ("Текстовые файлы", "*.txt"),
                        ("Текстовые файлы CSV", "*.csv"),
                        ("Все файлы", "*.*")])

        if filename:  # Если файл выбран
            self.label_error.config(text = "")
            self.label_path.config(text = f"Выбран файл: {filename}")
            self.process_file(filename)

    # Обработка выбранного файла
    def process_file (self, filename):
        """
        Параметры:
        filename (str): Абсолютный путь к открываемому файлу
        """

        with open(filename, "r", encoding = "utf-8") as file:
            try:
                self.data_lines = list(file)

                if len(self.data_lines) > self.length_content:
                    EncryptionWindow.progress_content(
                            self.textbox_content_scroll,
                            self.textbox_content,
                            self.data_lines)
                else:
                    EncryptionWindow.progress_content(
                            self.textbox_content,
                            self.textbox_content_scroll,
                            self.data_lines)

                self.label_load.config(
                        text = "Файл загружен",
                        foreground = "green")

            except FileInvalidCharacters as error:
                self.label_error.config(text = f"   Ошибка: {error}")
                self.label_load.config(
                        text = "Файл не загружен",
                        foreground = "red")
            except Exception:
                self.label_error.config(
                        text = f"   Ошибка: Не удалось открыть файл")
                self.label_load.config(
                        text = "Файл не загружен",
                        foreground = "red")

    @staticmethod
    # Перезапись текстового поля данными из выбранного файла
    def progress_content (textbox_on, textbox_off, data_lines):
        """
        Параметры:
        textbox_on (Text): Текстовое поле, в которое будут записаны данные
        textbox_off (Text): Текстовое поле, которое будет скрыто от пользователя
        data_lines (list): Список строк данных
        """
        textbox_on.config(state = "normal")
        textbox_on.delete('1.0', 'end')

        for index, line in enumerate(data_lines):
            # Проверка строки на неразрешенные символы
            text_chars = set(line)
            allowed_set = set(cypher.CHAR_ARRAY + "\n")
            invalid_chars = text_chars - allowed_set
            if invalid_chars != set(): raise FileInvalidCharacters(index + 1)

            if line != "\n":
                textbox_on.insert('end', line)

        textbox_on.config(state = tk.DISABLED)
        textbox_on.place(relwidth = 1, y = 110)
        textbox_off.place_forget()

    # Добавление новых строк в текстовое поле content
    def progress_add (self):
        self.data_lines.append(
                f"\n{self.textbox_add.get('1.0', 'end').rstrip('\n')}")

        if len(self.data_lines) > self.length_content:
            EncryptionWindow.progress_content(
                    self.textbox_content_scroll,
                    self.textbox_content,
                    self.data_lines)
        else:
            EncryptionWindow.progress_content(
                    self.textbox_content,
                    self.textbox_content_scroll,
                    self.data_lines)

        self.textbox_add.delete('1.0', 'end')

    # Расшифровать открытый файл
    def decrypt (self):
        data_lines_temp = self.data_lines
        for index, line in enumerate(data_lines_temp):
            data_lines_temp[index] = f"{cypher.decrypt(line.rstrip('\n'))}\n"
        self.data_lines = data_lines_temp

        if len(self.data_lines) > self.length_content:
            EncryptionWindow.progress_content(
                    self.textbox_content_scroll,
                    self.textbox_content,
                    self.data_lines)
        else:
            EncryptionWindow.progress_content(
                    self.textbox_content,
                    self.textbox_content_scroll,
                    self.data_lines)

    # Перезаписать открытый файл новым набором строк, предварительно их зашифровав
    def encrypt_save (self):
        try:
            with open(
                    self.label_path["text"].replace("Выбран файл: ", ""),
                    "w",
                    encoding = "utf-8") as file_result:
                for line in self.data_lines:
                    file_result.write(f"{cypher.encrypt(line.rstrip('\n'))}\n")

            # Перезапись текстового поля данными из перезаписанного файла
            self.process_file(
                    self.label_path["text"].replace("Выбран файл: ", ""))

        except (PermissionError, OSError):
            self.label_error.config(
                    text = f"   Ошибка: Файл недоступен для записи")

    # Сохранить набором строк в новый файл, предварительно их зашифровав
    def encrypt_save_as (self):
        try:
            # Вызов диалогового окна сохранения
            file_path = filedialog.asksaveasfilename(
                    title = "Сохранить файл",
                    filetypes = [
                            ("Текстовые файлы", "*.txt"),
                            ("Текстовые файлы CSV", "*.csv"),
                            ("Все файлы", "*.*")
                            ],
                    initialfile = "encrypt_2.txt",  # Файл по умолчанию
                    defaultextension = ".txt"
                    )

            with open(
                    file_path,
                    "w",
                    encoding = "utf-8") as file_result:
                for line in self.data_lines:
                    file_result.write(
                            f"{cypher.encrypt(line.rstrip('\n'))}\n")

            # Перезапись текстового поля данными из выбранного файла
            self.process_file(file_path)

        except (PermissionError, OSError):
            self.label_error.config(
                    text = f"   Ошибка: Файл недоступен для записи")

    def __init__ (self, setroot):
        # Вычисление количества строк для content
        temp = self.ID
        while len(temp) != 1:
            summ = 0
            for char in temp:
                summ += int(char)
            temp = str(summ)
        self.length_content = 10 + int(temp)

        # Создание текста для content
        index = 0
        text_content_line = ""
        while index < self.length_content - 1:
            index += 1
            text_content_line += f"{index}\n"
        if index == self.length_content - 1:
            text_content_line += f"{index + 1}"

        # Создание текста для content
        index = 0
        text_add_line = ""
        while index < self.length_add - 1:
            index += 1
            text_add_line += f"{index}\n"
        if index == self.length_add - 1:
            text_add_line += f"{index + 1}"

        self.root = setroot
        self.root.title("Шифрование текста")
        self.root.geometry(
                f"300x{290 + 16 * (self.length_content + self.length_add)}")
        main_frame = tk.Frame(setroot)
        main_frame.place(relwidth = 1, relheight = 1)

        # Текст - Вывод для ошибок
        self.label_error = tk.Label(
                main_frame,
                anchor = "w",
                foreground = "red",
                borderwidth = 0.5,
                relief = 'solid',
                wraplength = 300)
        self.label_error.pack(side = "bottom", fill = "x")

        # Текст - Путь к файлу
        self.label_path = tk.Label(
                main_frame,
                text = "Путь: ...",
                wraplength = 200)
        self.label_path.place(
                relx = 0.5,
                y = 80,
                height = 100,
                relwidth = 1,
                anchor = "center")

        # Текстовое поле - данные из файла без скроллинга
        self.textbox_content = tk.Text(
                main_frame, height = self.length_content,
                borderwidth = 0.5,
                relief = 'solid')
        self.textbox_content.insert('1.0', text_content_line)
        self.textbox_content.config(state = tk.DISABLED)
        self.textbox_content.place(relwidth = 1, y = 110)

        # Текстовое поле - данные из файла со скроллингом
        self.textbox_content_scroll = scroll_text.ScrolledText(
                main_frame, height = self.length_content,
                borderwidth = 0.5,
                relief = 'solid',
                state = tk.DISABLED)

        # Кнопка - «Загрузить файл»
        self.button_load = tk.Button(
                main_frame, text = "Загрузить файл",
                command = self.file_load)
        self.button_load.place(relx = 0.17, y = 12, height = 40, width = 100)

        # Текст - «Файл не загружен» Red / «Файл загружен» Green
        self.label_load = tk.Label(
                main_frame,
                text = "Файл не загружен",
                foreground = "red")
        self.label_load.place(relx = 0.53, y = 12, height = 40, width = 100)

        # Кнопка - «Расшифровать»
        self.button_decrypt = tk.Button(
                main_frame, text = "Расшифровать",
                command = self.decrypt)
        self.button_decrypt.place(
                x = 150,
                y = 120 + 16 * self.length_content,
                height = 25,
                width = 120)

        # Текст - «Новая строка»
        self.label = tk.Label(main_frame, text = "Новая строка", anchor = "w")
        self.label.place(
                x = 10,
                y = 145 + 16 * self.length_content,
                height = 20,
                relwidth = 0.5)

        # Текстовое поле - добавление новых строк
        self.textbox_add = tk.Text(
                main_frame, height = self.length_add,
                borderwidth = 0.5,
                relief = 'solid')
        self.textbox_add.insert('1.0', text_add_line)
        self.textbox_add.bind("<Button-1>", self.on_text_click)
        self.textbox_add.place(
                relwidth = 1,
                y = 170 + 16 * self.length_content)

        # Кнопка - «Добавить»
        self.button_load = tk.Button(
                main_frame, text = "Добавить",
                command = self.progress_add)
        self.button_load.place(
                x = 10,
                y = 185 + 16 * (self.length_content + self.length_add),
                height = 25,
                width = 70)

        # Кнопка - «Зашифровать и сохранить»
        self.button_encrypt_save = tk.Button(
                main_frame, text = "Зашифровать и сохранить",
                command = self.encrypt_save)
        self.button_encrypt_save.place(
                x = 100,
                y = 185 + 16 * (self.length_content + self.length_add),
                height = 25,
                width = 180)

        # Кнопка - Зашифровать и сохранить в новый файл
        self.button_encrypt_save = tk.Button(
                main_frame, text = "Зашифровать и сохранить как",
                command = self.encrypt_save_as)
        self.button_encrypt_save.place(
                x = 100,
                y = 220 + 16 * (self.length_content + self.length_add),
                height = 25,
                width = 180)

    # Обработчик события; Нажатие по текстовому полю — очищает содержимое при условии
    def on_text_click (self, _):
        if "1\n2\n" in self.textbox_add.get('1.0', 'end'):
            self.textbox_add.delete('1.0', 'end')


# Создание и запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    EncryptionWindow(root)
    root.mainloop()
