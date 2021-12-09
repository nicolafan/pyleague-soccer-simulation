# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from typing import List

from league import *
import simulation

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


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    setup_teams('serie_a.txt')
    league = League(name="Serie A", teams=teams)
    standings = {}
    for x in [y.team.identifier for y in league.participants]:
        standings[x] = 0
    for match_day in league.fixtures:
        for (x, y) in match_day:
            outcome = simulation.generate_outcome(league.get_team_by_id(x), league.get_team_by_id(y))
            if outcome == '1':
                standings[x] += 3
            elif outcome == 'X':
                standings[x] += 1
                standings[y] += 1
            else:
                standings[y] += 3
            print("{0}-{1} {2}".format(x, y, outcome))
            print("__________________________")
    final_standings = []
    for x in standings:
        final_standings.append((standings[x], x))
    final_standings.sort(reverse=True)
    for (x, y) in final_standings:
        print(y, x)
