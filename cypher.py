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

    print(f"Сдвиг: {shift}")

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

    print(f"Сдвиг: {shift}")

    for char in text:
        if char in CHAR_ARRAY:

            index = CHAR_ARRAY.index(char)
            new_index = (index - shift) % array_length
            decrypted.append(CHAR_ARRAY[new_index])

        else:
            # Оставить символы, не входящие в массив, без изменений
            decrypted.append(char)

    return ''.join(decrypted)
