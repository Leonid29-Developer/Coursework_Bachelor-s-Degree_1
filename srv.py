from operator import truediv

from flask import Flask, render_template as run, request, jsonify
import logging
from datetime import datetime
import os
import csv
import cypher  # модуль шифрования

# Настройка логирования

# Повторное создание папки для логов, если удалена
os.makedirs('logs', exist_ok = True)

# Обработчик для файла: DEBUG и выше
file_handler = logging.FileHandler('logs/requests.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(
        logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Обработчик для консоли: WARNING и выше
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)
console_handler.setFormatter(
        logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

logger = logging.getLogger(__name__)
logger.addHandler(file_handler)
logging.getLogger('werkzeug').addHandler(file_handler)
logger.addHandler(console_handler)


# Сохраняет сообщение в CSV‑файл
def save_csv (message):
    with open(
            'Data/messages.csv',
            'a',
            newline = '',
            encoding = 'utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([cypher.encrypt(message)])


app = Flask(__name__)


@app.route('/70220069/', methods = ['GET', 'POST'])
def home ():
    try:
        if request.method == 'POST':
            save_csv(request.form['text'])
        return run('encryption.html')

    except Exception:
        return run('error.html')


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000, debug = True)
    app.run(host = '127.0.0.1', port = 5000, debug = True)
