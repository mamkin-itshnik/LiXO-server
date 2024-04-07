import db_proxy as db
from models import Game


def new_game(session: str) -> Game:
    game_id = db.get_next_game_id()
    player = db.get_player_by_session(session)
    game = Game(game_id, player)
    db.add_new_game(game)
    return game_id


def get_game_for_player(game_id: int, session: str):
    game = db.get_game(game_id)
    if game:
        return game.for_player(session)


def make_move(session, game_id, move) -> bool:
    game = db.get_game(game_id)
    if game:
        if game.state != 'game':
            return False
        if game.board[move] != ' ':
            return False
        if game.playerA.session == session:
            game.set_cell(move, 'x')
        elif game.playerB.session == session:
            game.set_cell(move, 'o')
        else:
            return False
        return True
