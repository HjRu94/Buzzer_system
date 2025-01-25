import time
from typing import List, Union

from client.sound import SoundObject


class Player:
    """object representing a player."""

    def __init__(self, name='player', score=0, handicap=None):
        self.name: str = name
        self.score: int = score
        self.handicap: Union[int, None] = handicap
        self.handicap_time: float = float('inf')
        self.buzzer: bool = False
        self.buzzed_at: float = float('inf')
        self.sound: Union[SoundObject, None] = None
        self.wrong = False
        self.gpio_pin = None
        self.score = 0

    def set_name(self, name):
        self.name = name

    def set_score(self, score):
        self.score = score

    def buzz(self):
        if self.is_buzzed():
            return
        if self.wrong:
            return
        self.buzzer = True
        self.buzzed_at = time.time()

    def handicap_block(self):
        if self.handicap is not None:
            if time.time() - self.handicap_time < self.handicap:
                return True
        return False

    def unbuzz(self):
        self.buzzer = False
        self.buzzed_at = float('inf')

    def is_buzzed(self):
        return self.buzzer

    def set_wrong(self, wrong: bool):
        self.wrong = wrong

    def play_sound(self):
        if self.sound is not None:
            self.sound.play()

    def set_sound(self, sound: SoundObject):
        self.sound = sound

    def add_to_score(self):
        self.score += 1

    def sub_to_score(self):
        self.score -= 1

    def set_handicap(self, handicap: Union[int, None]):
        """Set the handicap of the player messured in seconds."""
        self.handicap = handicap


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
            player.set_wrong(False)

    def set_hadicap_time(self, handicap_time):
        for player in self:
            player.handicap_time = handicap_time

    def who_buzzed(self, timer_start) -> Union[int, None]:
        first_buzzed = None
        # set buzz time to maximum value
        buzz_time: float = float('inf')
        for i, player in enumerate(self):
            if player.is_buzzed() and not player.wrong and not player.handicap_block():
                if player.handicap is not None:
                    player_buzz_time = max(timer_start + player.handicap, player.buzzed_at)
                else:
                    player_buzz_time = player.buzzed_at
                if first_buzzed is None or player_buzz_time < buzz_time:
                    first_buzzed = i
                    buzz_time = player_buzz_time
        return first_buzzed

    def wrong_answer(self, timer_start):
        who_buzzed = self.who_buzzed(timer_start)
        if who_buzzed is None:
            return
        self[who_buzzed].set_wrong(True)

    def __getitem__(self, idx):
        return self.players[idx]

    def __iter__(self):
        return iter(self.players)
