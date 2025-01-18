from typing import List, Union


class Player:
    """object representing a player."""

    def __init__(self, name='player', score=0, handicap=None):
        self.name: str = name
        self.score: int = score
        self.handicap: Union[int, None] = handicap

    def set_name(self, name):
        self.name = name

    def set_score(self, score):
        self.score = score

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

    def __getitem__(self, idx):
        return self.players[idx]

    def __iter__(self):
        return iter(self.players)
