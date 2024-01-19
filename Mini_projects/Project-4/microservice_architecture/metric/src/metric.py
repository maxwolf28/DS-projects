import json
import pandas as pd
import pika
import numpy as np
 
try:
    # Создаём подключение к серверу на локальном хосте
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    # Объявляем очередь y_true
    channel.queue_declare(queue='y_true')
    # Объявляем очередь y_pred
    channel.queue_declare(queue='y_pred')
    df = pd.DataFrame(
        columns=["y_true", "y_pred"]
    )
   
    # Создаём функцию callback для обработки данных из очереди
    def callback(ch, method, properties, body):

        print(f'Из очереди {method.routing_key} получено значение {json.loads(body)["body"]}')
        with open('./logs/labels_log.txt', 'a') as f:
            f.write(f'Из очереди {method.routing_key} получено значение {json.loads(body)}\n')
        id = json.loads(body)['id']
        data = json.loads(body)["body"]
        if method.routing_key == "y_true":
            df.loc[id, "y_true"] = data
        else:
            df.loc[id, "y_pred"] = data

        if df.loc[id].isna().sum()==0:
            ae = np.abs(df.loc[id, "y_pred"]-df.loc[id, "y_true"])
            string = f"{id},{df.loc[id, 'y_true']},{df.loc[id, 'y_pred']},{ae}\n" 
            with open('./logs/metric_log.csv', 'a') as f:
                f.write(string)
                                
            df.drop(id)
          
    # Извлекаем сообщение из очереди y_true
    channel.basic_consume(
        queue='y_true',
        on_message_callback=callback,
        auto_ack=True
    )
    # Извлекаем сообщение из очереди y_pred
    channel.basic_consume(
        queue='y_pred',
        on_message_callback=callback,
        auto_ack=True
    )
    
    # Запускаем режим ожидания прихода сообщений
    print('...Ожидание сообщений, для выхода нажмите CTRL+C')
    channel.start_consuming()
except:
    print('Не удалось подключиться к очереди')