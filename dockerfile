# Выкачиваем из dockerhub облегченный образ с python версии 3.13
FROM python:3.13.0a6-alpine3.19
# Устанавливаем рабочую директорию для проекта в контейнере
WORKDIR /server
# Скачиваем/обновляем необходимые библиотеки для проекта 
COPY requirements.txt /server
RUN pip install -r requirements.txt
# |ВАЖНЫЙ МОМЕНТ| копируем содержимое папки, где находится Dockerfile, 
# в рабочую директорию контейнера
COPY . /server
# Переименовываем .env.example в .env (перенести в compose, наверное)
# ENTRYPOINT mv .env.example .env
# Устанавливаем порт, который будет использоваться для сервера
EXPOSE 5000
