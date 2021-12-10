import random

import typing

from pyleague import simulation
from pyleague.models import *


class League:

    def __init__(self, name: str, teams: List[Team]) -> None:
        self.fixtures: List[List[typing.Tuple[str, str]]] = []
        self.matchday = 0

        self.n_participants = len(teams)
        if self.n_participants % 2 == 1:
            raise ValueError('Number of teams must be even.')
        if self.n_participants < 1 or self.n_participants > 40:
            raise ValueError('Number of teams must be between 2 and 40.')
        identifiers = [team.identifier for team in teams]
        if len(identifiers) != len(set(identifiers)):
            raise ValueError('Identifiers must be unique.')
        self.name = name
        self.participants = []
        for team in teams:
            self.participants.append(Participant(team))

        self.generate_fixtures()

    def generate_fixtures(self):
        group_size = int(self.n_participants / 2)
        group_a = random.sample(self.participants, group_size)
        group_a = [p.team.identifier for p in group_a]
        group_b = [p.team.identifier for p in self.participants if p.team.identifier not in group_a]

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
        for (x, y) in self.fixtures[self.matchday]:
            outcome = simulation.generate_outcome(self.get_team_by_id(x), self.get_team_by_id(y))
            participant_a = self.get_participant_by_id(x)
            participant_b = self.get_participant_by_id(y)
            if outcome == '1':
                participant_a.points += 3
            elif outcome == '2':
                participant_b.points += 3
            else:
                participant_a.points += 1
                participant_b.points += 1

        self.matchday += 1
        self.print_standings()

    def print_standings(self):
        standings = [x for x in self.participants]
        standings.sort(key=lambda x: x.points, reverse=True)
        print('MATCHDAY {0}\n'.format(self.matchday))
        for x in standings:
            print('{0} {1}'.format(x.team.name, x.points))
        print('\n')
