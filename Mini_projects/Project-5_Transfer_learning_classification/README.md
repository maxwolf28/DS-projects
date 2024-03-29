# PROJECT-5. Transfer learning in solving the problem of flower classification

## Оглавление  
[1. Описание проекта](README.md#Описание-проекта)  
[2. Этапы работы над проектом](README.md#Этапы-работы-над-проектом)  
[3. Результаты](README.md#Результаты)    

## Описание проекта    

Датасет классификации цветов (http://www.robots.ox.ac.uk/~vgg/data/flowers/102/index.html) состоит из 102 видов цветов встречаемых в Великобритании. Для каждого класса есть от 40 до 258 примеров, чего мало для обучения модели для классификации с нуля.

Поэтому попробуем построить нашу модель с помощью transfer learning, на базе существующих  и уже обученных сетей.


[к оглавлению](README.md#Оглавление)


## Этапы работы над проектом    

Сначала построим baseline - модель в которой будет 3 блока слоев со схемой Сonv-Conv-Pooling, применим Batch - нормализацию, а также Dropout регуляризацию.
Используем и аугментацию входных данных.

Затем попробуем использовав Fine-tuning попробуем доучить под нашу задачу сеть EfficientNetB6 (достаточно сильная сеть, при том, что не сверх требовательна к ресурсам).

Будем оценивать результаты сетей по accuracy.

baseline в блокноте transfer-learning-keras-flowers-basa

fine-tuning сети в  transfer-learning-keras-flowers-efficientnet

[к оглавлению](README.md#Оглавление)


### Результаты

На Baseline при использовании классической архитектуры сверточной нейронной сети на валидации accuracy была - 29%. Ожидаемо слабый результат, так как данных было достаточно мало.
Но при использование Fine-tuning на базовой модели EfficientNetB6 (веса с ImageNet), (обучения в несколько шагов с постепенной разблокировкой слоев для обучения) с использованием аугментаций, и TTA, нам удалось построить сильную модель с заданной метрикой = 98%. 


[к оглавлению](README.md#Оглавление)


