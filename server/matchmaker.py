import os
import threading
from time import sleep

import db_proxy as db
from bots import dumbbot
from models import Game

BOT_ONLY = True if os.getenv('BOT_ONLY') == 'True' else False
MATCHMAKER = False


def _matchmaker(fast_bot: bool):
    waiting_list = []
    global MATCHMAKER
    MATCHMAKER = True
    while True:
        games = db.get_wait_games()
        for game in games:
            if fast_bot:
                start_bot(game)
            else:
                if waiting_list.count(game) > 10:
                    while game in waiting_list:
                        waiting_list.remove(game)
                    start_bot(game)
                else:
                    waiting_list.append(game)
        sleep(1)


def start_matchmaker():
    print('starting matchmaking')
    if not MATCHMAKER:
        threading.Thread(target=_matchmaker, args=(BOT_ONLY,), daemon=True).start()


def start_bot(game: Game):
    print('starting bot')
    threading.Thread(target=dumbbot, args=(game,), daemon=True).start()
