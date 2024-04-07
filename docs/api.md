# liXO server API

## Пример формата запроса

Аргументы передаются в соответствии с типом запроса: 

- GET - в url
- POST, PUT - в теле в json

Специфически передается сессия: в HTTP-заголовке X-Session

## Flow

1. Запросить сессию, потом пихать ее во все запросы
2. Начать новую игру
3. Получить текущее состояние игры:
  4. Дождаться, пока игра перейдет из состояния wait в game (=появился соперник)
  5. Если turn и you совпадают, то можно сделать ход
  6. Если игра перешла в состояние done, то она окончена (есть победитель или ничья)

## Endpoints

### Get new session

Request:
```
POST /session HTTP/1.1
Host: 127.0.0.1:5000
User-Agent: python-requests/2.31.0
Accept-Encoding: gzip, deflate, br
Accept: */*
Connection: close
Content-Length: 37
Content-Type: application/json

{"login": "user1", "password": "123"}
```

Response:
```
HTTP/1.1 200 OK
Server: Werkzeug/2.3.7 Python/3.11.3
Date: Sun, 07 Apr 2024 17:54:43 GMT
Content-Type: application/json
Content-Length: 52
Connection: close

{
  "session": "d3bfcafa69e94aa9b60817124b457760"
}
```


### Get new game

Request:
```
POST /new_game HTTP/1.1
Host: 127.0.0.1:5000
User-Agent: python-requests/2.31.0
Accept-Encoding: gzip, deflate, br
Accept: */*
Connection: close
X-Session: d3bfcafa69e94aa9b60817124b457760
Content-Length: 0


```

Response:
```
POST /new_game HTTP/1.1
Host: 127.0.0.1:5000
User-Agent: python-requests/2.31.0
Accept-Encoding: gzip, deflate, br
Accept: */*
Connection: close
X-Session: d3bfcafa69e94aa9b60817124b457760
Content-Length: 0


```

### Get game state

Запрос:
```
GET /game?game_id=0 HTTP/1.1
Host: 127.0.0.1:5000
User-Agent: python-requests/2.31.0
Accept-Encoding: gzip, deflate, br
Accept: */*
Connection: close
X-Session: d3bfcafa69e94aa9b60817124b457760


```

Ответ:
```
HTTP/1.1 200 OK
Server: Werkzeug/2.3.7 Python/3.11.3
Date: Sun, 07 Apr 2024 17:54:43 GMT
Content-Type: application/json
Content-Length: 91
Connection: close

{
  "board": "         ",
  "game_id": 0,
  "state": "wait",
  "turn": "x",
  "you": "x"
}

```

- board — текущее состояние поля, просто соединенные в строку x, o или " ", слева направо сверху вниз
- state — возможные варианты:
  - wait — ожидание соперника
  - game — игра в процессе
  - done — игра завершена (есть победитель или ничья)
- turn — чья сейчас очередь ходить
- you — за кого играет пользователь
- winner — победитель (если есть, то x или o; если нет, то None)

### Make a move

Request:
```
PUT /make_move HTTP/1.1
Host: 127.0.0.1:5000
User-Agent: python-requests/2.31.0
Accept-Encoding: gzip, deflate, br
Accept: */*
Connection: close
X-Session: d3bfcafa69e94aa9b60817124b457760
Content-Length: 25
Content-Type: application/json

{"game_id": 0, "move": 1}
```

Response:
```
HTTP/1.1 200 OK
Server: Werkzeug/2.3.7 Python/3.11.3
Date: Sun, 07 Apr 2024 17:54:46 GMT
Content-Type: application/json
Content-Length: 19
Connection: close

{
  "move": "ok"
}

```

move — число от 0 до 8, номер клетки, нумеруются слева направо сверху вниз. При успешном ходе (если клетка не занята) при запросе `/game` в ответе в строке board пробел по этому индексу заменится на соответствующий игроку символ. Пример начала партии:

1. board: "         "
2. move: 1
3. board: " x       "
4. ход соперника
5. board: " xo      "
6. move: 8
7. board: " xo     x"
