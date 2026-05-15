import tkinter as tk
from dbm import error
from os import remove
from tkinter import filedialog, messagebox as msgbox, scrolledtext as stext


class EncryptionWindow:
    length = "70220069"  # ID студента
    Data = ""  # Обрабатываемые данные (текст)

    def file_load (self):
        # Открывает диалоговое окно выбора файла
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

    def process_file (self, filename):
        # Обработка выбранного файла

        with open(filename, "r", encoding = "utf-8") as file:
            try:
                content = file.read()
                self.Data = content

                if content.count('\n') + 1 > self.length:
                    self.content_set(
                            self.textbox_content_scroll,
                            self.textbox_content,
                            content)
                else:
                    self.content_set(
                            self.textbox_content_scroll,
                            self.textbox_content,
                            content)

                raise  # вызов ошибки

            except Exception:
                self.label_error.config(
                        text = f"   Ошибка: Не удалось открыть файл")

    def content_set (self, textbox_on, textbox_off, content):
        textbox_on.config(state = "normal")
        textbox_on.delete('1.0', 'end')
        textbox_on.insert('1.0', content)
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
        textline = ""
        while index < self.length - 1:
            index += 1
            textline += f"{index}\n"
        if index == self.length - 1:
            textline += f"{index + 1}"

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
                relief = 'solid')
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
        self.textbox_content.insert('1.0', textline)
        self.textbox_content.config(state = tk.DISABLED)
        self.textbox_content.place(relwidth = 1, y = 110)

        # Текстовое поле - данные из файла с скроллингом
        self.textbox_content_scroll = stext.ScrolledText(
                main_frame, height = self.length,
                borderwidth = 0.5,
                relief = 'solid')  # ,
        #   state = tk.DISABLED
        # self.textbox_content_scroll.place(relwidth = 1, y = 90)
        # self.textbox_content_scroll.place_forget()
        # self.textbox_content_scroll.place()

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
