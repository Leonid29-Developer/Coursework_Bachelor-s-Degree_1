from idlelib.iomenu import encoding
from operator import truediv

from flask import Flask, render_template as run, request, jsonify
import logging
from datetime import datetime
import os
import csv
import cypher  # Модуль шифрования

# Настройка логирования

# Повторное создание папки для логов, если удалена
os.makedirs('logs', exist_ok = True)

# Обработчик для файла: DEBUG и выше
file_handler = logging.FileHandler('logs/requests.log', encoding = 'utf-8')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(
        logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Обработчик для консоли: WARNING и выше
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)
console_handler.setFormatter(
        logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logging.getLogger('werkzeug').addHandler(file_handler)
logger.addHandler(console_handler)


# Поиск индекса, начиная с 1
def find_missing_index (array):
    min_value = min(array)
    max_value = max(array)
    missing_set = set(range(min_value, max_value + 2)) - set(array)
    return min(missing_set)


# Получение свободного индекса, поиск не занятых начиная с 1
def get_index ():
    if os.path.getsize('Data/messages.csv') > 0:
        index_array = []
        with open('Data/messages.csv', 'r', encoding = 'utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                index_array.append(int(row[1]))
        return find_missing_index(index_array)

    else: return 1


# Сохраняет сообщение в CSV‑файл
def save_csv (ip, message):
    with open(
            'Data/messages.csv',
            'a',
            newline = '',
            encoding = 'utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
                [datetime.now().strftime('%Y-%m-%d %H:%M:%S'), get_index(), ip,
                 cypher.encrypt(message)])


app = Flask(__name__)


@app.route('/')
def main ():
    return run('main.html')

@app.route('/70220069/', methods = ['GET', 'POST'])
def home ():
    try:
        if request.method == 'POST':
            save_csv(request.remote_addr, request.form['text'])
            return run('result.html', msg = request.form['text'])

        else: return run('encryption.html')

    except Exception:
        return run('error.html')


@app.route('/reset/', methods = ['GET', 'POST'])
def reset ():
    if request.method == 'POST' and os.path.exists('Data/messages.csv'):
        os.remove('Data/messages.csv')
    return run('reset.html')


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000, debug = True)
    app.run(host = '127.0.0.1', port = 5000, debug = True)
