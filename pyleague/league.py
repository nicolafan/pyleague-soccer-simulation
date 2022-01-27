import random

import typing
from typing import Optional

from pyleague import simulation
from pyleague.models import *


class League:
    def __init__(self, name: str, teams: List[Team]) -> None:
        self.fixtures: List[List[typing.Tuple[str, str]]] = []
        self.matchday = 0

        self.n_participants = len(teams)
        if self.n_participants % 2 == 1:
            raise ValueError("Number of teams must be even.")
        if self.n_participants < 1 or self.n_participants > 40:
            raise ValueError("Number of teams must be between 2 and 40.")
        identifiers = [team.identifier for team in teams]
        if len(identifiers) != len(set(identifiers)):
            raise ValueError("Identifiers must be unique.")
        self.name = name
        self.participants = []
        for team in teams:
            self.participants.append(Participant(team))

        self._generate_fixtures()

    def _generate_fixtures(self):
        group_size = int(self.n_participants / 2)
        group_a = random.sample(self.participants, group_size)
        group_a = [p.team.identifier for p in group_a]
        group_b = [
            p.team.identifier
            for p in self.participants
            if p.team.identifier not in group_a
        ]

        random.shuffle(group_a)
        random.shuffle(group_b)

        for i in range(self.n_participants - 1):
            self.fixtures.append([])

            for j in range(group_size):
                fixture = (group_a[j], group_b[j])
                if i % 2 == 1:
                    fixture = (group_b[j], group_a[j])
                self.fixtures[i].append(fixture)

            t1 = group_b[0]
            group_b = group_b[1:] + group_b[:1]
            group_a = group_a[-1:] + group_a[:-1]
            t2 = group_a[0]
            group_a[0] = group_a[1]
            group_a[1] = t1
            group_b[group_size - 1] = t2

            random.shuffle(self.fixtures[i])

        for i in range(self.n_participants - 1):
            second_round = [(y, x) for (x, y) in self.fixtures[i]]
            self.fixtures.append(second_round)

    def get_team_by_id(self, identifier: str) -> Team:
        return [x.team for x in self.participants if x.team.identifier == identifier][0]

    def get_participant_by_id(self, identifier: str) -> Participant:
        return [x for x in self.participants if x.team.identifier == identifier][0]

    def generate_matchday(self):
        if self.matchday >= self.n_participants * 2 - 2:
            print("The championship has ended!")
            return
        for (x, y) in self.fixtures[self.matchday]:
            participant_a = self.get_participant_by_id(x)
            participant_b = self.get_participant_by_id(y)
            outcome = simulation.generate_outcome(
                participant_a.team, participant_b.team
            )

            if outcome == "1":
                participant_a.add_win()
                participant_b.add_loss()
            elif outcome == "2":
                participant_a.add_loss()
                participant_b.add_win()
            else:
                participant_a.add_draw()
                participant_b.add_draw()

            goals_home, goals_away = simulation.generate_result(
                participant_a.team, participant_b.team, outcome
            )
            print(
                participant_a.team.name,
                goals_home,
                "-",
                goals_away,
                participant_b.team.name,
            )
            participant_a.goals_scored += goals_home
            participant_a.goals_conceded += goals_away
            participant_b.goals_scored += goals_away
            participant_b.goals_conceded += goals_home

        self.matchday += 1
        # self._print_standings()

    def _print_standings(self):
        standings = [x for x in self.participants]
        standings.sort(key=lambda x: x.points, reverse=True)
        print("MATCHDAY {0}\n".format(self.matchday))
        for x in standings:
            print("{0} {1}".format(x.team.name, x.points))
        print("\n")

    def get_standings(self):
        standings = [x for x in self.participants]
        standings.sort(key=lambda x: x.points, reverse=True)
        return standings


league: Optional[League] = None


def create_league(name: str, teams: List[Team]):
    global league
    league = League(name, teams)
    return league
