import os
import string

# Создание массива символов в заданном порядке
CHAR_ARRAY = (
        '0123456789' +  # Цифры
        'абвгдеёжзийклмнопрстуфхцчшщъыьэюя' +  # Малые русские
        'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ' +  # Большие русские
        'abcdefghijklmnopqrstuvwxyz' +  # Малые латинские
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ' +  # Большие латинские
        string.punctuation +  # Пунктуация
        ' '  # Пробел
)


def encrypt (text, sid = 70220069):
    """
    Шифрует текстовое сообщение с помощью кода Цезаря (сдвиг вправо)

    Параметры:
    text (str): Исходное текстовое сообщение для шифрования
    sid (int): ID от значения которого будет вычисляться размер сдвига
        (по умолчанию 70220069)

    Возвращает:
    str: Зашифрованное сообщение.
    """

    encrypted = []
    # Длина массива символов
    array_length = len(CHAR_ARRAY)
    # Размер сдвига
    shift = sid % 11

    for char in text:
        if char in CHAR_ARRAY:
            index = CHAR_ARRAY.index(char)
            new_index = (index + shift) % array_length
            encrypted.append(CHAR_ARRAY[new_index])

        else:
            # Оставить символы, не входящие в массив, без изменений
            encrypted.append(char)

    return ''.join(encrypted)


def decrypt (text, sid = 70220069):
    """
    Дешифрует текстовое сообщение с помощью кода Цезаря (сдвиг влево).

    Параметры:
    text (str): Исходное текстовое сообщение для шифрования
    sid (int): ID от значения которого будет вычисляться размер сдвига
        (по умолчанию 70220069)

    Возвращает:
    str: Зашифрованное сообщение.
    """

    decrypted = []
    # Длина массива символов
    array_length = len(CHAR_ARRAY)
    # Размер сдвига
    shift = sid % 11

    for char in text:
        if char in CHAR_ARRAY:
            index = CHAR_ARRAY.index(char)
            new_index = (index - shift) % array_length
            decrypted.append(CHAR_ARRAY[new_index])

        else:
            # Оставить символы, не входящие в массив, без изменений
            decrypted.append(char)

    return ''.join(decrypted)


def process_files ():
    """Обрабатывает файлы encrypt.txt и decrypt.txt
    записывает результаты в файлы encrypt_result.txt и decrypt_result.txt"""

    # Обработка файла для шифрования
    if os.path.exists("Data/encrypt.txt"):
        index = 0
        with open("Data/encrypt.txt", "r", encoding = "utf-8") as f:
            with open(
                    "Data/encrypt_result.txt", "w",
                    encoding = "utf-8") as f_result:
                for line in f:
                    index += 1
                    text_result = (f"Тестовый кейс зашифровки - {index}:\n" +
                                   f"ID студента: 70220069\n" +
                                   f"Исходный текст: {line.rstrip('\n')}\n" +
                                   f"Зашифрованный текст: {encrypt(line).rstrip('\n')}\n")

                    if index > 1:
                        f_result.write("\n" + text_result)
                    else:
                        f_result.write(text_result)

                    # Дублирование содержимого файла с результатом в консоль.
                    print(text_result)
    else:
        print("<<<Файл encrypt.txt не найден>>>")

    # Обработка файла для дешифрования
    if os.path.exists("Data/decrypt.txt"):
        index = 0
        with open("Data/decrypt.txt", "r", encoding = "utf-8") as f:
            with open(
                    "Data/decrypt_result.txt", "w",
                    encoding = "utf-8") as f_result:
                for line in f:
                    index += 1
                    text_result = (f"Тестовый кейс дешифрования - {index}:\n" +
                                   f"ID студента: 70220069\n" +
                                   f"Исходный текст: {line.rstrip('\n')}\n" +
                                   f"Расшифрованный текст: {decrypt(line).rstrip('\n')}\n")

                    if index > 1:
                        f_result.write("\n" + text_result)
                    else:
                        f_result.write(text_result)

                    # Дублирование содержимого файла с результатом в консоль.
                    print(text_result)
    else:
        print("<<<Файл decrypt.txt не найден>>>")


if __name__ == "__main__":
    print(
            f"{"=" * 60}\nЗапуск модуля напрямую. Обработка файлов encrypt.txt и" +
            f" decrypt.txt\n{"=" * 60}")
    process_files()
    print(
            f"{"=" * 60}\nОбработка завершена. Результаты записаны в encrypt_result.txt" +
            f" и decrypt_result.txt\n{"=" * 60}")
