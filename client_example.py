import requests

SERVER = 'http://127.0.0.1:5000'
TMP_SESSION = '111'


def print_board(board):
    # {
    #     'board': 'xo       ',
    #     'you': 'x',
    #     'turn': 'x',
    # }
    for y in range(3):
        line = board['board'][y*3:y*3+3]
        line = '|'.join(line)
        print(line)
        print('------')




def new_game(session: str):
    r = requests.get(f'{SERVER}/new_game', params={'session': session})
    if r.status_code == 200:
        return r.json()


def get_board(session: str, game_id: int):
    r = requests.get(f'{SERVER}/get_board', params={'session': session, 'game_id': game_id})
    if r.status_code == 200:
        return r.json()


def new_and_get():
    s = get_session({})
    g = new_game(s)
    gid = g['game_id']
    b = get_board(s, gid)
    board = b['']
    print(board)


def get_session(auth: dict):
    return TMP_SESSION


if __name__ == '__main__':
    get_session({1: 2})
