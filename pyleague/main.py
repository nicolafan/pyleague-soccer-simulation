# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import csv
from pyleague.league import *

teams: List[Team] = []

def setup_teams(filename):
    """Sets up teams for game simulation by reading information in from the lega_a.csv file and subsequently parses them and then loads them into the global teams list by creating Team objects for each of them.

    :param filename: the file path to the file containing information about the teams
    :type filename: string

    :raises FileNotFoundError: will raise a FileNotFoundError if the file is not found in the path specified
    """
    # Read CSV file
    with open(filename) as fp:
        reader = csv.reader(fp, delimiter=",", quotechar='"')
        lines = [row for row in reader]

    for line in lines:
        identifier, name, sv, ap, dp = line
        teams.append(Team(identifier, name, int(sv), int(ap), int(dp)))


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    setup_teams("../lega_a.csv")
    league = create_league(name="Lega A", teams=teams)
    print(league)
    import pyleague.interface