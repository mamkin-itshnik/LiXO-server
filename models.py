import db_proxy as db


class Board:
    def __init__(self, game_id, player):
        self.game_id = game_id
        self.playerA = player
        self.playerB = None
        self.board = '         '


class Player:
    def __init__(self, session):
        self.sessions = db.get_previous_sessions_by_session(session)
        self.sessions.append(session)
        self.last_session = session
