import random


class Team:
    form_value = 0

    def __init__(self, identifier, name, strength_value, attack_power, defense_power):
        self.identifier = identifier
        self.name = name
        self.strength_value = strength_value
        self.attack_power = attack_power
        self.defense_power = defense_power


class Participant:
    points = 0
    goals_scored = 0
    goals_conceded = 0
    last_results = []

    def __init__(self, team):
        self.team = team


class League:
    fixtures = []

    def __init__(self, name, teams):
        self.name = name
        self.participants = []
        for team in teams:
            self.participants.append(Participant(team))
        self.n_participants = len(self.participants)
        self.generate_fixtures()

    def generate_fixtures(self):
        group_size = int(self.n_participants/2)
        group_a = random.sample(self.participants, group_size)
        group_a = [p.team.identifier for p in group_a]
        group_b = [p.team.identifier for p in self.participants if p.team.identifier not in group_a]

        random.shuffle(group_a)
        random.shuffle(group_b)

        for i in range(self.n_participants-1):
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
            group_b[group_size-1] = t2

            random.shuffle(self.fixtures[i])

        for i in range(self.n_participants-1):
            second_round = [(y, x) for (x, y) in self.fixtures[i]]
            self.fixtures.append(second_round)



