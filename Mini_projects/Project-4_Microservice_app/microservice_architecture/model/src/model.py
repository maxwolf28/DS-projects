import pika
import pickle
import numpy as np
import json

try:
    with open('myfile.pkl', 'rb') as pkl_file:
        regressor = pickle.load(pkl_file)
        
except:
    print('Не удалось open file with model')
    
try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    # Объявляем очередь features
    channel.queue_declare(queue='features')
    channel.queue_declare(queue='y_pred')
    # print("ready to get message")
    # Создаём функцию callback для обработки данных из очереди y_pred
    def callback(ch, method, properties, body):
        # print("got message")
        print(f'Получен вектор признаков {json.loads(body)["body"]}')
        features = np.asarray(json.loads(body)['body']).reshape(1,-1)
        pred = regressor.predict(features)
        message = {
            "id" : json.loads(body)["id"],
            "body" : pred[0]
        }
        channel.basic_publish(
            exchange='',
            routing_key='y_pred',
            body=json.dumps(message)
        )
        print(f'Предсказание {pred[0]} отправлено в очередь y_pred')


    # Извлекаем сообщение из очереди features
    # on_message_callback показывает, какую функцию вызвать при получении сообщения
    channel.basic_consume(
        queue='features',
        on_message_callback=callback,
        auto_ack=True
    )
    print('...Ожидание сообщений, для выхода нажмите CTRL+C')

    # Запускаем режим ожидания прихода сообщений
    channel.start_consuming()
except:
    print('Не удалось подключиться к очереди')