import tkinter as tk
from tkinter import (filedialog, messagebox as msgbox,
                     scrolledtext as scroll_text)


class EncryptionWindow:
    length = "70220069"  # ID студента
    data_lines = ""  # Обрабатываемые данные (текст)

    # Открывает диалоговое окно выбора файла
    def file_load (self):
        filename = filedialog.askopenfilename(
                title = "Загрузить файл",
                initialdir = "./Data/",  # Начальная директория
                initialfile = "encrypt.txt",  # Файл по умолчанию
                filetypes = [
                        ("Текстовые файлы", "*.txt"),
                        ("Все файлы", "*.*")])

        if filename:  # Если файл выбран
            self.label_path.config(text = f"Выбран файл: {filename}")
            self.process_file(filename)

    # Обработка выбранного файла
    def process_file (self, filename):
        with open(filename, "r", encoding = "utf-8") as file:
            try:
                self.data_lines = list(file)

                if len(self.data_lines) > self.length:
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

            except Exception:
                self.label_error.config(
                        text = f"   Ошибка: Не удалось открыть файл")

    @staticmethod
    # Перезапись текстового поля данными из выбранного файла
    def progress_content (textbox_on, textbox_off, data_lines):
        textbox_on.config(state = "normal")
        textbox_on.delete('1.0', 'end')

        for index, line in enumerate(data_lines):
            if line != "\n":
                textbox_on.insert('end', line)

        textbox_on.config(state = tk.DISABLED)
        textbox_on.place(relwidth = 1, y = 110)
        textbox_off.place_forget()

    def __init__ (self, setroot):
        # Вычисление количества строк и создание текста
        temp = self.length
        while len(temp) != 1:
            summ = 0
            for char in temp:
                summ += int(char)
            temp = str(summ)
        self.length = 10  # int(temp) +
        index = 0
        text_line = ""
        while index < self.length - 1:
            index += 1
            text_line += f"{index}\n"
        if index == self.length - 1:
            text_line += f"{index + 1}"

        self.root = setroot
        self.root.title("Шифрование текста")
        self.root.geometry(f"300x{40 * self.length}")

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
                anchor = "center"
                )

        # Текстовое поле - данные из файла без скроллинга
        self.textbox_content = tk.Text(
                main_frame, height = self.length,
                borderwidth = 0.5,
                relief = 'solid')
        self.textbox_content.insert('1.0', text_line)
        self.textbox_content.config(state = tk.DISABLED)
        self.textbox_content.place(relwidth = 1, y = 110)

        # Текстовое поле - данные из файла со скроллингом
        self.textbox_content_scroll = scroll_text.ScrolledText(
                main_frame, height = self.length,
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


# Создание и запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    EncryptionWindow(root)
    root.mainloop()
