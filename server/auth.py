from uuid import uuid4

import db_proxy as db


def is_session_valid(session: str):
    print(f'fake session check: {session=}')
    return True


def new_session(login, password):
    sess = uuid4().hex
    print('ask for session:', login, password, '->', sess)
    return True, sess


def is_game_available_for_session(game_id, session) -> bool:
    print('is_game_available_for_session', game_id, session)
    game = db.get_game(game_id)
    players_sessions = [game.playerA.session]
    try:
        players_sessions.append(game.playerB.session)
    except AttributeError:
        pass
    if session in players_sessions:
        return True
    else:
        return False
