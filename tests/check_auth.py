import os
import sys
from pprint import pprint

import requests
from dotenv import load_dotenv

SERVER = ''
BAD_REQUEST = 'bad request'
BAD_GAME = 'error with new game'


def get_vars():
    # env vars should be like: http 1.1.1.1 12345 /qawwedfweferg/
    global SERVER
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    SERVER = f"{os.getenv('SCHEMA')}://{os.getenv('HOST')}:{os.getenv('PORT')}{os.getenv('URL_PATH')}"


def check_and_parse(req):
    if req.status_code == 200:
        return req.json()
    else:
        print(req.status_code)
        pprint(dict(req.headers))
        if len(req.content) < 100:
            pprint(req.content)
        return None


def get_session(auth: dict):
    req = requests.post(SERVER + 'session', json=auth)
    j = check_and_parse(req)
    if j:
        return j['session']
    else:
        return BAD_REQUEST


def new_game(session):
    req = requests.post(SERVER + 'new_game', headers={'X-Session': session})
    j = check_and_parse(req)
    if j:
        return j['game_id']
    else:
        return BAD_GAME


def main():
    get_vars()

    # b = get_session({'login': os.getenv('BAD_USER'), 'password': os.getenv('BAD_PASSWORD')})
    # if b != BAD_REQUEST:
    #     print('bad user/pass passed')
    #     sys.exit(1)
    s = get_session({'login': os.getenv('GOOD_USER'), 'password': os.getenv('GOOD_PASSWORD')})
    if s == BAD_REQUEST:
        print('good user/pass declined')
        sys.exit(2)
    github_env = os.getenv('GITHUB_ENV')
    if github_env:
        with open(github_env, 'a') as w:
            w.write(f'TOKEN={s}\n')
    else:
        with open('token.tmp', 'w') as w:
            w.write(s)

    # b = new_game('huita')
    # if b != BAD_GAME:
    #     print('bad session passed')
    #     sys.exit(3)
    g = new_game(s)
    if g == BAD_GAME:
        print('good session declined')
        sys.exit(4)

    print('ok')
    sys.exit(0)


if __name__ == '__main__':
    main()
