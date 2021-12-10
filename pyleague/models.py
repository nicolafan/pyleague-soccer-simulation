from typing import List


class Team:

    def __init__(self, identifier: str, name: str, strength_value: int, attack_power: int, defense_power: int):
        self.form_value = 0
        self.consecutive_w = 0
        self.consecutive_l = 0

        self.identifier = identifier
        self.name = name
        self.strength_value = strength_value
        self.attack_power = attack_power
        self.defense_power = defense_power

    def add_win(self):
        if self.consecutive_l > 0:
            self.consecutive_l = 0
        if self.consecutive_w < 3:
            self.form_value += 5
        elif self.form_value > 0:
            self.form_value -= 5
        self.consecutive_w += 1

    def add_draw(self):
        self.consecutive_w = 0
        self.consecutive_l = 0
        self.form_value = 0

    def add_loss(self):
        if self.consecutive_w > 0:
            self.consecutive_w = 0
        if self.consecutive_l < 3:
            self.form_value -= 3
        elif self.form_value < 0:
            self.form_value += 3
        self.consecutive_l += 1


class Participant:

    def __init__(self, team):
        self.points = 0
        self.goals_scored = 0
        self.goals_conceded = 0
        self.last_results: List[int] = []

        self.team = team
