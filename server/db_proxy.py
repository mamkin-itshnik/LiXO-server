from threading import Lock
from typing import Optional

from models import Player, Game

players = []
games = []
db_mutex = Lock()


def with_lock(db_func):
    def wrapper(*args, **kwargs):
        db_mutex.acquire()
        res = db_func(*args, **kwargs)
        db_mutex.release()
        return res

    return wrapper


@with_lock
def get_player_by_session(session: str):
    for player in players:
        if player.session == session:
            return player
    player = Player(session)
    players.append(player)
    return player


@with_lock
def get_next_game_id():
    if len(games) == 0:
        return 0
    last = max(games, key=lambda x: x.game_id)
    return last.game_id + 1


@with_lock
def add_new_game(game: Game):
    games.append(game)


@with_lock
def get_game(game_id: int) -> Optional[Game]:
    for game in games:
        if game.game_id == game_id:
            return game
    return None


@with_lock
def get_wait_games():
    ret = []
    for game in games:
        if game.state == 'wait':
            ret.append(game)
    return ret
