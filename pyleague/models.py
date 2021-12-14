from typing import List


class Team:
    def __init__(
        self,
        identifier: str,
        name: str,
        strength_value: int,
        attack_power: int,
        defense_power: int,
    ):
        self.form_value = 0
        self.last_results: List[str] = []

        self.identifier = identifier
        self.name = name
        self.strength_value = strength_value
        self.attack_power = attack_power
        self.defense_power = defense_power

    def add_win(self):
        if len(self.last_results) == 5:
            del self.last_results[0]
        self.last_results.append("W")
        self.form_value = 0
        for j in range(len(self.last_results) - 1, -1, -1):
            if self.last_results[j] == "W":
                self.form_value += 5
                if self.form_value == 15:
                    break
            else:
                break

    def add_draw(self):
        if len(self.last_results) == 5:
            del self.last_results[0]
        self.last_results.append("D")
        self.form_value = 0

    def add_loss(self):
        if len(self.last_results) == 5:
            del self.last_results[0]
        self.last_results.append("L")
        self.form_value = 0
        for j in range(len(self.last_results) - 1, -1, -1):
            if self.last_results[j] == "L":
                self.form_value -= 3
                if self.form_value == -9:
                    break
            else:
                break


class Participant:
    def __init__(self, team):
        self.points = 0
        self.goals_scored = 0
        self.goals_conceded = 0
        self.wins = 0
        self.draws = 0
        self.losses = 0
        self.last_results: List[int] = []

        self.team = team

    def add_win(self):
        self.team.add_win()
        self.points += 3
        self.wins += 1

    def add_draw(self):
        self.team.add_draw()
        self.points += 1
        self.draws += 1

    def add_loss(self):
        self.team.add_loss()
        self.losses += 1
