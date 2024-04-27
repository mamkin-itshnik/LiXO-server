# Выкачиваем из dockerhub облегченный образ с python версии 3.13
FROM python:3.13.0a6-alpine3.19
# Устанавливаем рабочую директорию для проекта в контейнере
WORKDIR /app
# Скачиваем/обновляем необходимые библиотеки для проекта 
COPY requirements.txt .
RUN pip install -r requirements.txt
# |ВАЖНЫЙ МОМЕНТ| копируем содержимое папки, где находится Dockerfile, 
# в рабочую директорию контейнера
COPY . .
# Переименовываем .env в .env (перенести в compose, наверное)
#ENTRYPOINT ["mv", "/app/server/.env.example", "/app/server/.env"]
# Запускаем сервер, когда запускается образ
CMD ["python", "server/server.py"]
# Устанавливаем порт, который будет использоваться для сервера
EXPOSE 5000
