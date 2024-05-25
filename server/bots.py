import random
from time import sleep

import auth
import db_proxy as db
from game import make_move
from models import Game


def dumbbot(game: Game):
    s = auth.new_session('bot', '123')
    p = db.get_player_by_session(s)
    game.become_opponent(p)
    while game.state == 'game':
        info = game.for_player(s)
        if info['turn'] == info['you']:
            move = random.randint(0, 8)
            ok = make_move(s, game.game_id, move)
            if ok:
                sleep(1)
        else:
            sleep(1)
    print(game.winner, 'wins')
