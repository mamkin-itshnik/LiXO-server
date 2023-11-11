from flask import Flask, jsonify, request, abort
import auth
import game
import db_proxy as db

app = Flask(__name__)


@app.route('/')
def index():
    return 'Flask is running!'


@app.route('/new_game', methods=['GET'])
def new_game():
    if 'session' not in request.args:
        abort(400)
    session = request.args['session']
    if not auth.is_session_valid(session):
        abort(401)
    player = db.get_player_by_session(session)
    game_id = game.new_game(player)
    return jsonify({'game_id': game_id})


@app.route('/board', methods=['GET'])
def get_board():
    if 'session' not in request.args:
        abort(400)
    if 'game_id' not in request.args:
        abort(400)
    session = request.args['session']
    game_id = request.args['game_id']
    if not auth.is_session_valid(session):
        abort(401)
