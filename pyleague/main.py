# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from pyleague.league import *

teams: List[Team] = []


def setup_teams(filename):
    with open(filename) as f:
        lines = f.readlines()
    for line in lines:
        elements = line.split(" ")
        if len(elements) > 5:
            elements = elements[:-1]
        identifier, name, sv, ap, dp = elements
        teams.append(Team(identifier, name, int(sv), int(ap), int(dp)))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    setup_teams('serie_a.txt')
    league = League(name="Serie A", teams=teams)
    for i in range(0, 38):
        league.generate_matchday()
