import csv
import json
import logging
import os
from datetime import datetime
from flask import Flask, render_template as run, request, Response
import cypher  # Модуль шифрования

# Настройка логирования

# Повторное создание папки для логов, если удалена
os.makedirs('logs', exist_ok = True)

# Обработчик для файла: DEBUG и выше

file_handler = logging.FileHandler('logs/server.log', encoding = 'utf-8')
file_handler.setLevel(logging.DEBUG)
# noinspection SpellCheckingInspection
file_handler.setFormatter(
        logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Обработчик для консоли: WARNING и выше
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)
# noinspection SpellCheckingInspection
console_handler.setFormatter(
        logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logging.getLogger('werkzeug').addHandler(file_handler)
logger.addHandler(console_handler)


# Создает файл CSV с нужными заголовками (первой строкой)
def create_csv (filename):
    if not os.path.isfile(filename):
        with open(
                filename,
                'a',
                newline = '',
                encoding = 'utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["datetime", "id", "ip", "text"])


app = Flask(__name__)


@app.route('/')
def main ():
    return run('main.html')


# Поиск индекса, начиная с 1
def find_missing_index (array):
    min_value = min(array)
    max_value = max(array)
    missing_set = set(range(min_value, max_value + 2)) - set(array)
    return min(missing_set)


# Получение свободного индекса, поиск не занятых начиная с 1
def get_index (filename):
    if os.path.getsize(filename) > 21:
        index_array = []
        with open(filename, 'r', encoding = 'utf-8') as file:
            file.readline()
            reader = csv.reader(file)
            for row in reader:
                index_array.append(int(row[1]))
        return find_missing_index(index_array)

    else: return 1


# Сохраняет сообщение в CSV‑файл
def save_csv (ip, message, filename):
    create_csv(filename)
    with open(
            filename,
            'a',
            newline = '',
            encoding = 'utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
                [datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                 get_index(filename), ip,
                 cypher.encrypt(message)])


# noinspection PyBroadException
@app.route('/70220069/', methods = ['GET', 'POST'])
def home ():
    try:
        if request.method == 'POST':
            save_csv(
                    request.remote_addr,
                    request.form['text'],
                    'Data/messages.csv')
            return run('result.html', msg = request.form['text'])

        else: return run('encryption.html')

    except Exception:
        return run('error.html')


@app.route('/hidden/', methods = ['POST'])
def hidden_home ():
    save_csv(
            request.form['ip'],
            request.form['text'],
            request.form['filename'])
    return


@app.route('/reset/', methods = ['GET', 'POST'])
def reset ():
    if request.method == 'POST' and os.path.exists('Data/messages.csv'):
        os.remove('Data/messages.csv')
    return run('reset.html')


# Чтение данных файла CSV для JSON
def read_csv (decrypt):
    data = []
    with open('Data/messages.csv', 'r', encoding = 'utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if decrypt:
                row['text'] = cypher.decrypt(row['text'])
            data.append(row)
    return data


# noinspection PyBroadException
@app.route('/get_all.json/', methods = ['GET'])
def get_all ():
    try:
        json_output = json.dumps(
                read_csv(False),
                ensure_ascii = False,
                indent = 2)
        return Response(
                json_output,
                mimetype = 'application/json; charset=utf-8')
    except Exception:
        return run('error.html')


# noinspection PyBroadException
@app.route('/get_all_decrypted.json/', methods = ['GET'])
def get_all_decrypted ():
    try:
        json_output = json.dumps(
                read_csv(True),
                ensure_ascii = False,
                indent = 2)
        return Response(
                json_output,
                mimetype = 'application/json; charset=utf-8')
    except Exception:
        return run('error.html')


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000, debug = True)
    app.run(host = '127.0.0.1', port = 5000, debug = True)
