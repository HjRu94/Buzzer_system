import time
from typing import List, Union


class Player:
    """object representing a player."""

    def __init__(self, name='player', score=0, handicap=None):
        self.name: str = name
        self.score: int = score
        self.handicap: Union[int, None] = handicap
        self.buzzer: bool = False
        self.buzzed_at: float = float('inf')

    def set_name(self, name):
        self.name = name

    def set_score(self, score):
        self.score = score

    def buzz(self):
        if self.is_buzzed():
            return 0
        self.buzzer = True
        self.buzzed_at = time.time()

    def unbuzz(self):
        self.buzzer = False
        self.buzzed_at = float('inf')

    def is_buzzed(self):
        return self.buzzer

    def set_handicap(self, handicap: Union[int, None]):
        """Set the handicap of the player messured in seconds."""
        self.handicap = handicap

    def add_to_score(self, points):
        self.score += points


class Players:
    """object representing multiple players."""

    def __init__(self, n_players=2):
        self.n_players = n_players
        self.players = self.create_players(n_players)

    def create_players(self, n_players: int) -> List[Player]:
        return [Player() for _ in range(n_players)]

    def reset_buzzers(self):
        for player in self:
            player.unbuzz()

    def who_buzzed(self) -> Union[int, None]:
        first_buzzed = None
        # set buzz time to maximum value
        buzz_time: float = float('inf')
        for i, player in enumerate(self):
            if player.is_buzzed():
                if first_buzzed is None:
                    first_buzzed = i
                    buzz_time = player.buzzed_at
                elif player.buzzed_at < buzz_time:
                    first_buzzed = i
                    buzz_time = player.buzzed_at
        return first_buzzed

    def __getitem__(self, idx):
        return self.players[idx]

    def __iter__(self):
        return iter(self.players)
