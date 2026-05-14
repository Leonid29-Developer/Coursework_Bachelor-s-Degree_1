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


def encrypt(text, sid=70220069):
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


def decrypt(text, sid=70220069):
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


if __name__ == "__main__":
    print("=" * 40 + "\nТЕСТИРОВАНИЕ МОДУЛЯ ШИФРОВАНИЯ ЦЕЗАРЯ\n" + "=" * 40)

    # Тестовый кейс зашифровки - 1
    text = "Квартира78"
    print(f"Тестовый кейс зашифровки - 1:\n" +
          f"Исходное: {text}\n" +
          f"Зашифровано: {encrypt(text)}\n")

    # Тестовый кейс зашифровки - 2
    text = "Кофе)йнОе@утро"
    print(f"Тестовый кейс зашифровки - 2:\n" +
          f"Исходное: {text}\n" +
          f"Зашифровано: {encrypt(text)}\n")

    # Тестовый кейс зашифровки - 3
    text = "loGin2*24"
    print(f"Тестовый кейс зашифровки - 3:\n" +
          f"Исходное: {text}\n" +
          f"Зашифровано: {encrypt(text)}\n")

    # Тестовый кейс дешифрования - 1
    text = "ъТпЭж67бв"  # уЛиЦа 045
    print(f"Тестовый кейс дешифрования - 1:\n" +
          f"Исходное: {text}\n" +
          f"Расшифровано: {decrypt(text)}\n")

    # Тестовый кейс дешифрования - 2
    text = "*тлЩх#чжКхшщГ6/O7tl:"  # #леТоVраДость (H0me)
    print(f"Тестовый кейс дешифрования - 2:\n" +
          f"Исходное: {text}\n" +
          f"Расшифровано: {decrypt(text)}\n")

    # Тестовый кейс дешифрования - 3
    text = "WhZz$vYk>ёNё"  # PaSsWoRd-9G9
    print(f"Тестовый кейс дешифрования - 3:\n" +
          f"Исходное: {text}\n" +
          f"Расшифровано: {decrypt(text)}\n")

    print("=" * 40 + "\nВсе тесты завершены\n" + "=" * 40)
