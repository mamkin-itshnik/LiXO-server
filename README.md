# LiXO-server
![LiXo](https://github.com/mamkin-itshnik/LiXO-server/actions/workflows/cicd-prod.yml/badge.svg)
![LiXo](https://github.com/mamkin-itshnik/LiXO-server/actions/workflows/cicd-test.yml/badge.svg)
## API

[Описание API](docs/api.md)

## Завести

1. Переименовать `.env.example` в `.env`
2. Если нужна видимость извне — исправить в `.env` IP-адрес 127.0.0.1 на необходимый
3. (Опционально) Настроить venv 
4. Установить зависимости `pip install -r requirements.txt`
5. Перейти в папку server и запустить `python server.py`

## Боты

На текущий момент реализован только тупой бот (dumbbot), который просто в свою очередь пытается сделать ход в рандомную клетку. 

## Клиенты

Для примера реализован client_example.py, который ведет себя как тупой бот. 
При запуске client_example.py необходимо передать ему IP и порт сервера в виде 
python client_example.py x.x.x.x xxxx

https://github.com/mamkin-itshnik/lixo-android
