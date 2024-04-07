import random
from threading import RLock
from typing import Optional


class Player:
    def __init__(self, session):
        self.session: str = session


class Game:
    def __init__(self, game_id, player):
        self.game_id = game_id
        self.playerA: Player = player
        self.playerB: Optional[Player] = None
        self.board: str = '         '
        self.mutex = RLock()

    # def _check_equality(self, arr: list[int]):
    #     assert max(arr) < 9
    #     assert min(arr) >= 0
    #     vals = [self.board[i] for i in arr]
    #     head, *tail = vals
    #     if all([head == i for i in tail]) and head != ' ':
    #         return head
    #     else:
    #         return None
    def _check_equality(self, arr: list[int]):
        assert max(arr) < 9
        assert min(arr) >= 0
        assert len(arr) == 3
        self.mutex.acquire()
        vals = [self.board[i] for i in arr]
        if vals[0] == vals[1] and vals[0] == vals[2] and vals[0] != ' ':
            ret = vals[0]
        else:
            ret = None
        self.mutex.release()
        return ret

    def for_player(self, session):
        res = {'game_id': self.game_id,
               'board': self.board,
               'you': 'x' if self.playerA.session == session else 'o',
               'turn': self.turn,
               'state': self.state
               }
        if self.state == 'done':
            res['winner'] = self.winner
        return res

    @property
    def _non_empty(self) -> str:
        self.mutex.acquire()
        res = self.board.replace(' ', '')
        self.mutex.release()
        return res

    @property
    def turn(self):
        if len(self._non_empty) % 2 == 0:
            return 'x'
        else:
            return 'o'

    @property
    def winner(self) -> Optional[str]:
        possible_lines = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6],
        ]
        for line in possible_lines:
            if winner := self._check_equality(line):
                return winner
        return None

    @property
    def state(self) -> str:
        self.mutex.acquire()
        if self.playerB is None:
            ret = 'wait'
        elif self.winner is None and self.board.count(' ') != 0:
            ret = 'game'
        else:
            ret = 'done'
        self.mutex.release()
        return ret

    def become_opponent(self, opponent: Player):
        self.mutex.acquire()
        print('become_opponent', self.game_id, opponent.session)
        assert self.playerB is None
        self.playerB = opponent
        if random.choice([1, 2, 3]) == 3:
            print('swap players')
            self.playerA, self.playerB = self.playerB, self.playerA
        self.mutex.release()

    def set_cell(self, move: int, val: str):
        self.mutex.acquire()
        assert self.board[move] == ' '
        assert len(val) == 1
        assert move >= 0
        assert move < len(self.board)
        head, tail = self.board[:move], self.board[move + 1:]
        self.board = head + val + tail
        self.mutex.release()
