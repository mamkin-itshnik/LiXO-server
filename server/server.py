# import db_proxy as db
import os
from typing import Optional

from dotenv import load_dotenv
from flask import Flask, request, abort

import auth
import game
from matchmaker import start_matchmaker

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
app = Flask(__name__)
DEBUG = True if os.getenv('DEBUG') == 'True' else False
HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))


def check_session(r) -> tuple[bool, Optional[dict], Optional[int]]:
    if 'X-Session' not in r.headers:
        return False, {'error': 'no session'}, 400
    session = r.headers['X-Session']
    if not auth.is_session_valid(session):
        return False, {'error': 'bad session'}, 401
    return True, None, None


@app.route('/')
def index():
    return 'Flask is running!!'


@app.route('/new_game', methods=['POST'])
def new_game():
    ok, resp, code = check_session(request)
    if not ok:
        return resp, code
    else:
        game_id = game.new_game(request.headers['X-Session'])
        return {'game_id': game_id}


@app.route('/game', methods=['GET'])
def get_game():
    ok, resp, code = check_session(request)
    if not ok:
        return resp, code
    else:
        session = request.headers['X-Session']
        if 'game_id' not in request.args:
            return {'error': 'no game_id'}, 400
        game_id = int(request.args['game_id'])
        if not auth.is_game_available_for_session(game_id, session):
            return {'error': 'it\'s not your game'}, 403
        _game = game.get_game_for_player(game_id, session)
        if _game:
            print(_game)
            return _game
        abort(500)


@app.route('/session', methods=['POST'])
def get_session():
    if 'login' not in (json := request.json):
        return {'error': 'no login'}, 400
    if 'password' not in json:
        return {'error': 'no password'}, 400
    res, session = auth.new_session(json['login'], json['password'])
    if res:
        return {'session': session}
    else:
        return {'error': 'bad login or password'}, 401


@app.route('/make_move', methods=['PUT'])
def make_move():
    ok, resp, code = check_session(request)
    if not ok:
        return resp, code
    else:
        session = request.headers['X-Session']
        if 'game_id' not in request.json:
            return {'error': 'no game_id'}, 400
        game_id = request.json['game_id']
        if not auth.is_game_available_for_session(game_id, session):
            return {'error': 'it\'s not your game'}, 403
        if 'move' not in request.json:
            return {'error': 'no move'}, 400
        move = request.json['move']
        if move < 0 or move > 8:
            return {'error': 'move is out of range'}, 403
        if game.make_move(session, game_id, move):
            return {'move': 'ok'}
        else:
            return {'error': 'bad move'}, 403


def main():
    start_matchmaker()
    return app
    
if __name__ == '__main__':
    _app = main()
    _app.run(debug=DEBUG, host=HOST, port=PORT)
# 400 Bad Request
# 401 Unauthorized
# 403 Forbidden
# 404 Not Found
# 500 Internal Server Error