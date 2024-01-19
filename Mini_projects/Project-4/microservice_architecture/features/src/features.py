import json
import time
from datetime import datetime

import numpy as np
import pika
from sklearn.datasets import load_diabetes


np.random.seed(42)
X,y = load_diabetes(return_X_y=True)


while True:
    try:
        random_row = np.random.randint(0,X.shape[0]-1)
        message_id = datetime.timestamp(datetime.now())
        message_y_true = {
            'id' : message_id,
            'body' : y[random_row]
        }
        message_features = {
            'id' : message_id,
            'body' : list(X[random_row])
        }
        # Подключение к серверу на локальном хосте:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', credentials=pika.credentials.PlainCredentials('guest', 'guest', erase_on_connect=False)))
        channel = connection.channel()

        # Создаём очередь y_true
        channel.queue_declare(queue='y_true')

        # Публикуем сообщение
        channel.basic_publish(exchange='',
                            routing_key='y_true',
                            body=json.dumps(message_y_true))
        print('Сообщение с правильным ответом отправлено в очередь')

        # Создаём очередь features
        channel.queue_declare(queue='features')

        # Публикуем сообщение
        channel.basic_publish(exchange='',
                            routing_key='features',
                            body=json.dumps(message_features))
        print('Сообщение с вектором признаков отправлено в очередь')

        # Закрываем подключение
        connection.close()
        time.sleep(3)
    except:
        print('Не удалось подключиться к очереди')