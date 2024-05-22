import random
import sys
from pprint import pprint
from time import sleep
import requests
if len(sys.argv) < 3:
    HOST = '127.0.0.1'
    PORT = '5001'
else:
    HOST = sys.argv[1]
    PORT = sys.argv[2]

SERVER = 'http://'+HOST+':'+PORT
# PROXY = {'http': 'http://127.0.0.1:8080'}
PROXY = None


def check_and_parse(req):
    if req.status_code == 200:
        return req.json()
    else:
        print(req.status_code)
        pprint(dict(req.headers))
        if len(req.content) < 100:
            pprint(req.content)
        return None


def print_game(game):
    # {
    #     'game_id': 1,
    #     'board': 'xo       ',
    #     'you': 'x',
    #     'turn': 'x',
    #     'state': 'game'
    # }
    for y in range(3):
        line = game['board'][y * 3:y * 3 + 3]
        line = '|'.join(line)
        print(line)
        print('------')


def get_session(auth: dict):
    req = requests.post(SERVER + '/session', json=auth, proxies=PROXY)
    j = check_and_parse(req)
    if j:
        return j['session']
    else:
        return 'error with session'


def new_game(session):
    req = requests.post(SERVER + '/new_game', headers={'X-Session': session}, proxies=PROXY)
    j = check_and_parse(req)
    if j:
        return j['game_id']
    else:
        return 'error with new game'


def still_game(session, game_id):
    req = requests.get(SERVER + '/game?game_id=' + str(game_id), headers={'X-Session': session}, proxies=PROXY)
    j = check_and_parse(req)
    if j and j['state'] == 'game':
        return True
    else:
        print(j)
        return False


def wait_opponent(session, game_id):
    while True:
        req = requests.get(SERVER + '/game?game_id=' + str(game_id), headers={'X-Session': session}, proxies=PROXY)
        j = check_and_parse(req)
        if not j:
            return
        if j['state'] != 'wait':
            break
        sleep(1)


if __name__ == '__main__':
    s = get_session({'login': 'user1', 'password': '123'})
    print(f'{s=}')
    gid = new_game(s)
    print(f'{gid=}')
    wait_opponent(s, gid)
    print('game begin')
    move_counter = 0
    while last := still_game(s, gid):
        if move_counter > 20:
            print('too much moves')
            sys.exit(1)
        r = requests.get(SERVER + '/game?game_id=' + str(gid), headers={'X-Session': s}, proxies=PROXY)
        j = check_and_parse(r)
        if j['turn'] == j['you']:
            while True:
                move = random.randint(0, 8)
                print('i\'ll take', move)
                rr = requests.put(SERVER + '/make_move', json={'game_id': gid, 'move': move}, headers={'X-Session': s},
                                  proxies=PROXY)
                jj = check_and_parse(r)
                if jj:
                    print_game(jj)
                    break
                sleep(1)
            move_counter += 1
        else:
            print('wait his move')
        sleep(1)
