import os
import random
import sys
from pprint import pprint
from time import sleep, time

import requests
from dotenv import load_dotenv

SERVER = ''
MAX_DURATION = 120


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


def get_vars():
    # env vars should be like: http 1.1.1.1 12345 /qawwedfweferg/
    global SERVER
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    SERVER = f"{os.getenv('SCHEMA')}://{os.getenv('HOST')}:{os.getenv('PORT')}{os.getenv('URL_PATH')}"


def new_game(session):
    req = requests.post(SERVER + 'new_game', headers={'X-Session': session})
    j = check_and_parse(req)
    if j:
        return j['game_id']
    else:
        print('bad new game')
        sys.exit(3)


def still_game(session, game_id):
    req = requests.get(SERVER + 'game?game_id=' + str(game_id), headers={'X-Session': session})
    j = check_and_parse(req)
    if j and j['state'] == 'game':
        return True
    else:
        print(j)
        return False


def wait_opponent(session, game_id):
    while True:
        req = requests.get(SERVER + 'game?game_id=' + str(game_id), headers={'X-Session': session})
        j = check_and_parse(req)
        if not j:
            return
        if j['state'] != 'wait':
            break
        sleep(1)


def main():
    get_vars()
    github_env = os.getenv('GITHUB_ENV')
    if github_env:
        token = os.getenv('TOKEN')
        if not token:
            print('wtf? Is previous test executed?')
            sys.exit(1)
    else:
        token = open('token.tmp').read()
    gid = new_game(token)
    print(f'{gid=}')
    wait_opponent(token, gid)
    print('game begin')
    begin = time()
    while still_game(token, gid):
        if time() - begin > MAX_DURATION:
            print('game is too long')
            sys.exit(2)
        r = requests.get(SERVER + 'game?game_id=' + str(gid), headers={'X-Session': token})
        j = check_and_parse(r)
        if j['turn'] == j['you']:
            while True:
                move = random.randint(0, 8)
                print('i\'ll take', move)
                rr = requests.put(SERVER + 'make_move', json={'game_id': gid, 'move': move},
                                  headers={'X-Session': token})
                jj = check_and_parse(r)
                if jj:
                    print_game(jj)
                    break
                sleep(1)
        else:
            print('wait his move')
        sleep(1)
    print('ok')
    sys.exit(0)


if __name__ == '__main__':
    main()
