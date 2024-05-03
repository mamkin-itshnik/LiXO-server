# Выкачиваем из dockerhub облегченный образ с python версии 3.13
FROM python:alpine
# Устанавливаем рабочую директорию для проекта в контейнере
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN adduser -D appuser
USER appuser
COPY . .
# Переименовываем .env в .env (перенести в compose, наверное)
#ENTRYPOINT ["mv", "/app/server/.env.example", "/app/server/.env"]
# Запускаем сервер, когда запускается образ
#CMD ["python", "server/server.py"]
# Устанавливаем порт, который будет использоваться для сервера
#EXPOSE 5000
