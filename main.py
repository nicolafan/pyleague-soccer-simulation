# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from league import Team, League

teams = []


def setup_teams(filename):
    with open(filename) as f:
        lines = f.readlines()
    for line in lines:
        elements = line.split(" ")
        if len(elements) > 5:
            elements = elements[:-1]
        identifier, name, sv, ap, dp = elements
        teams.append(Team(identifier, name, sv, ap, dp))


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    setup_teams('serie_a.txt')
    league = League(name="Serie A", teams=teams)
    print(len(league.fixtures))
    for x in league.fixtures:
        for y in x:
            print(y)
        print('-----------------------------')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
