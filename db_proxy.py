from models import Player, Board


players = []
boards = []


def get_player_by_session(session: str):
    for player in players:
        if player.last_session == session:
            return player
    player = Player(session)
    players.append(player)
    return player


def get_previous_sessions_by_session(session: str):  # wtf?
    for player in players:
        if player.last_session == session:
            return player.sessions
    return []


def get_next_game_id():
    if len(boards) == 0:
        return 0
    last = max(boards, key=lambda x: x.game_id)
    return last.game_id + 1


def save_board(board: Board):
    boards.append(board)
