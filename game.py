import db_proxy as db
from models import Board, Player


def new_game(player: Player):
    game_id = db.get_next_game_id()
    board = Board(game_id, player)
    db.save_board(board)
    return game_id